import React from 'react';
import { cn } from '../lib/utils';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function MetricCard({ label, value, trend, trendValue, icon: Icon, color }) {
  const isPositive = trend === 'up';
  
  return (
    <div className="glass-card p-6 rounded-2xl space-y-4">
      <div className="flex justify-between items-start">
        <div className={cn("p-3 rounded-xl", color)}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div className={cn(
          "flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-full",
          isPositive ? "bg-green-500/10 text-green-400" : "bg-red-500/10 text-red-400"
        )}>
          {isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
          {trendValue}%
        </div>
      </div>
      
      <div>
        <p className="text-sm text-muted-foreground font-medium">{label}</p>
        <h3 className="text-2xl font-bold mt-1 tracking-tight">{value}</h3>
      </div>
      
      <div className="w-full bg-secondary/30 h-1.5 rounded-full overflow-hidden">
        <div 
          className={cn("h-full rounded-full transition-all duration-500", color.replace('bg-', 'bg-opacity-100 bg-'))} 
          style={{ width: '70%' }} 
        />
      </div>
    </div>
  );
}
