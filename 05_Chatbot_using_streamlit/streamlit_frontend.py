import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk
import groq
import uuid
import sqlite3


DB_PATH = 'chatbot_memory.db'


# -----------------------------------------------------------------------------
# DATABASE HELPERS
# -----------------------------------------------------------------------------

def get_db_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def ensure_names_table():
    """Create thread_names table if it does not exist yet."""
    db = get_db_connection()
    db.execute("""
        CREATE TABLE IF NOT EXISTS thread_names (
            thread_id TEXT PRIMARY KEY,
            name      TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()


def get_all_threads():
    """Return list of (thread_id, display_name) ordered by most recent first."""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            SELECT c.thread_id, COALESCE(n.name, 'New Chat') AS name
            FROM (
                SELECT DISTINCT thread_id
                FROM checkpoints
                ORDER BY checkpoint_id DESC
            ) c
            LEFT JOIN thread_names n ON c.thread_id = n.thread_id
        """)
        rows = cursor.fetchall()
        db.close()
        return rows
    except Exception:
        return []


def set_thread_name(thread_id, name):
    """Insert or update the display name for a thread."""
    db = get_db_connection()
    db.execute("""
        INSERT INTO thread_names (thread_id, name)
        VALUES (?, ?)
        ON CONFLICT(thread_id) DO UPDATE SET name = excluded.name
    """, (thread_id, name))
    db.commit()
    db.close()


def thread_has_name(thread_id):
    """Check if a thread already has a custom name set."""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM thread_names WHERE thread_id = ?", (thread_id,))
        row = cursor.fetchone()
        db.close()
        return row is not None
    except Exception:
        return False


def delete_thread(thread_id):
    """Delete a thread and all its data from all tables."""
    db = get_db_connection()
    db.execute("DELETE FROM checkpoints  WHERE thread_id = ?", (thread_id,))
    db.execute("DELETE FROM writes       WHERE thread_id = ?", (thread_id,))
    db.execute("DELETE FROM thread_names WHERE thread_id = ?", (thread_id,))
    db.commit()
    db.close()


def auto_name_from_message(message):
    """Generate a short chat title from the first user message (like ChatGPT)."""
    clean = message.strip().replace('\n', ' ')
    if len(clean) <= 40:
        return clean
    # Truncate at word boundary
    truncated = clean[:40]
    last_space = truncated.rfind(' ')
    if last_space > 20:
        truncated = truncated[:last_space]
    return truncated + '...'


def load_history_from_langgraph(thread_id):
    """Load past messages from LangGraph checkpointer for a given thread."""
    config = {'configurable': {'thread_id': thread_id}}
    try:
        state = chatbot.get_state(config)
        messages = state.values.get('messages', [])
        history = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                history.append({'role': 'user', 'content': msg.content})
            elif isinstance(msg, AIMessage):
                history.append({'role': 'assistant', 'content': msg.content})
        return history
    except Exception:
        return []


# -----------------------------------------------------------------------------
# ONE-TIME SETUP
# -----------------------------------------------------------------------------
ensure_names_table()


# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'thread_id' not in st.session_state:
    threads = get_all_threads()
    st.session_state['thread_id'] = threads[0][0] if threads else str(uuid.uuid4())

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = load_history_from_langgraph(
        st.session_state['thread_id']
    )

if 'open_menu' not in st.session_state:
    st.session_state['open_menu'] = None

if 'renaming' not in st.session_state:
    st.session_state['renaming'] = None


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("My Conversations")
    st.divider()

    if st.button("New Chat", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        st.session_state['thread_id'] = new_id
        st.session_state['message_history'] = []
        st.session_state['open_menu'] = None
        st.session_state['renaming'] = None
        st.rerun()

    st.divider()
    st.markdown("**Sessions**")

    all_threads = get_all_threads()

    if not all_threads:
        st.caption("No saved sessions yet.")
    else:
        for thread_id, display_name in all_threads:
            is_active = thread_id == st.session_state['thread_id']
            menu_open = st.session_state['open_menu'] == thread_id
            is_renaming = st.session_state['renaming'] == thread_id

            col_chat, col_menu = st.columns([5, 1])

            with col_chat:
                # Bold the active chat name to indicate current session
                label = f"**{display_name}**" if is_active else display_name
                if st.button(label, key=f"open_{thread_id}", use_container_width=True):
                    st.session_state['thread_id'] = thread_id
                    st.session_state['message_history'] = load_history_from_langgraph(thread_id)
                    st.session_state['open_menu'] = None
                    st.session_state['renaming'] = None
                    st.rerun()

            with col_menu:
                if st.button("...", key=f"menu_{thread_id}"):
                    if menu_open:
                        st.session_state['open_menu'] = None
                        st.session_state['renaming'] = None
                    else:
                        st.session_state['open_menu'] = thread_id
                        st.session_state['renaming'] = None
                    st.rerun()

            # Action panel — visible only when ... is clicked for this thread
            if menu_open:
                if is_renaming:
                    new_name = st.text_input(
                        "New name",
                        value=display_name,
                        key=f"rename_input_{thread_id}",
                        label_visibility="collapsed"
                    )
                    save_col, cancel_col = st.columns(2)
                    with save_col:
                        if st.button("Save", key=f"save_{thread_id}", use_container_width=True):
                            if new_name.strip():
                                set_thread_name(thread_id, new_name.strip())
                            st.session_state['open_menu'] = None
                            st.session_state['renaming'] = None
                            st.rerun()
                    with cancel_col:
                        if st.button("Cancel", key=f"cancel_{thread_id}", use_container_width=True):
                            st.session_state['open_menu'] = None
                            st.session_state['renaming'] = None
                            st.rerun()
                else:
                    action_col1, action_col2 = st.columns(2)
                    with action_col1:
                        if st.button("Rename", key=f"rename_{thread_id}", use_container_width=True):
                            st.session_state['renaming'] = thread_id
                            st.rerun()
                    with action_col2:
                        if st.button("Delete", key=f"delete_{thread_id}", use_container_width=True):
                            delete_thread(thread_id)
                            if thread_id == st.session_state['thread_id']:
                                remaining = get_all_threads()
                                if remaining:
                                    st.session_state['thread_id'] = remaining[0][0]
                                    st.session_state['message_history'] = load_history_from_langgraph(
                                        remaining[0][0]
                                    )
                                else:
                                    st.session_state['thread_id'] = str(uuid.uuid4())
                                    st.session_state['message_history'] = []
                            st.session_state['open_menu'] = None
                            st.rerun()


# -----------------------------------------------------------------------------
# MAIN CHAT AREA
# -----------------------------------------------------------------------------
st.title("LangGraph Chatbot")

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input("Type your message here...")

if user_input:

    # Check if this is the first message in a new thread (before saving name)
    is_new_thread = not thread_has_name(st.session_state['thread_id'])

    # Auto-name this chat from the first message (like ChatGPT does)
    if is_new_thread:
        auto_name = auto_name_from_message(user_input)
        set_thread_name(st.session_state['thread_id'], auto_name)

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        try:
            def stream_tokens():
                for chunk, metadata in chatbot.stream(
                    {'messages': [HumanMessage(content=user_input)]},
                    config=CONFIG,
                    stream_mode="messages"
                ):
                    if isinstance(chunk, AIMessageChunk) and chunk.content:
                        yield chunk.content

            ai_message = st.write_stream(stream_tokens())
            st.session_state['message_history'].append(
                {'role': 'assistant', 'content': ai_message}
            )

            # Rerun after first message so sidebar refreshes and shows the new chat
            if is_new_thread:
                st.rerun()

        except groq.RateLimitError as e:
            error_msg = str(e)
            if "Request too large" in error_msg:
                st.warning("Request too large. Your message exceeded the token limit. Try asking something shorter.")
            elif "rate_limit_exceeded" in error_msg:
                st.warning("Rate limit reached. Too many requests. Please wait a moment and try again.")
            else:
                st.warning(f"Groq Rate Limit Error: {error_msg}")

        except groq.AuthenticationError:
            st.error("Invalid API Key. Please check your GROQ_API_KEY in the .env file.")

        except groq.APIConnectionError:
            st.error("Connection Error. Could not reach Groq API. Check your internet connection.")

        except groq.APIStatusError as e:
            st.error(f"Groq API Error (status {e.status_code}): {e.message}")

        except Exception as e:
            st.error(f"Unexpected Error: {str(e)}")