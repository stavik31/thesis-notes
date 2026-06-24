import pandas as pd                                                                                                                                                                                                                                                         
import numpy as np                                                                                                                                                                                                                                                          
from sklearn.cluster import DBSCAN                                                                                                                                                                                                                                          
import folium                                                                                                                                                                                                                                                               
from folium.plugins import HeatMap                                                                                                                                                                                                                                          
import matplotlib                                                                                                                                                                                                                                                           
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path                                                                                                                                                                                                                                                    
   
DATA_DIR = Path('/home/vik-esoc/Desktop/thesis/data')                                                                                                                                                                                                                       
OUT_DIR  = Path('/home/vik-esoc/Desktop/thesis/analysis')
OUT_DIR.mkdir(exist_ok=True)                                                                                                                                                                                                                                                
                  
# ── Load ──────────────────────────────────────────────────────────────────────                                                                                                                                                                                            
print("Loading...")
collision = pd.read_csv(                                                                                                                                                                                                                                                    
    DATA_DIR / 'dft-road-casualty-statistics-collision-last-5-years.csv',                                                                                                                                                                                                   
    low_memory=False                                                                                                                                                                                                                                                        
)                                                                                                                                                                                                                                                                           
collision = collision.dropna(subset=['latitude', 'longitude', 'collision_severity'])                                                                                                                                                                                        
collision = collision[                                                                                                                                                                                                                                                      
    (collision['latitude']  != 0) &
    (collision['longitude'] != 0) &                                                                                                                                                                                                                                         
    (collision['collision_severity'].isin([1, 2, 3]))                                                                                                                                                                                                                       
]
collision['severity_score'] = 4 - collision['collision_severity']                                                                                                                                                                                                           
print(f"  {len(collision):,} crashes")                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                              
uk_centre = [collision['latitude'].mean(), collision['longitude'].mean()]                                                                                                                                                                                                   
                                                                                                                                                                                                                                                                              
# ── MAP 1: Severity-weighted heatmap ─────────────────────────────────────────                                                                                                                                                                                             
print("Building heatmap...")
sample    = collision.sample(n=min(100_000, len(collision)), random_state=42)                                                                                                                                                                                               
heat_data = sample[['latitude', 'longitude', 'severity_score']].values.tolist()                                                                                                                                                                                             
   
m1 = folium.Map(location=uk_centre, zoom_start=6, tiles='CartoDB dark_matter')                                                                                                                                                                                              
HeatMap(        
    heat_data,                                                                                                                                                                                                                                                              
    min_opacity=0.3,
    radius=8,
    blur=12,                                                                                                                                                                                                                                                                
    max_zoom=14,
    gradient={0.2: 'blue', 0.45: 'cyan', 0.65: 'lime', 0.85: 'yellow', 1.0: 'red'}                                                                                                                                                                                          
).add_to(m1)                                                                                                                                                                                                                                                                
m1.save(OUT_DIR / 'heatmap.html')
print("  → heatmap.html")                                                                                                                                                                                                                                                   
                  
# ── DBSCAN ────────────────────────────────────────────────────────────────────                                                                                                                                                                                            
print("Running DBSCAN (~1-2 min)...")
coords = np.radians(collision[['latitude', 'longitude']].values)                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                              
db = DBSCAN(
    eps=0.5 / 6371.0,   # 500m in radians                                                                                                                                                                                                                                   
    min_samples=50,                                                                                                                                                                                                                                                         
    algorithm='ball_tree',
    metric='haversine',                                                                                                                                                                                                                                                     
    n_jobs=-1   
).fit(coords)

collision['cluster'] = db.labels_                                                                                                                                                                                                                                           
n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print(f"  {n_clusters:,} clusters found")                                                                                                                                                                                                                                   
print(f"  {(db.labels_ == -1).mean()*100:.1f}% of crashes outside any cluster")                                                                                                                                                                                             
                                                                                                                                                                                                                                                                              
# ── Cluster stats ─────────────────────────────────────────────────────────────                                                                                                                                                                                            
hotspot     = collision[collision['cluster'] != -1]                                                                                                                                                                                                                         
non_hotspot = collision[collision['cluster'] == -1]                                                                                                                                                                                                                         
   
cluster_stats = (                                                                                                                                                                                                                                                           
    hotspot.groupby('cluster')
    .agg(
        crash_count =('collision_severity', 'count'),                                                                                                                                                                                                                       
        fatal_pct   =('collision_severity', lambda x: (x == 1).mean() * 100),
        serious_pct =('collision_severity', lambda x: (x == 2).mean() * 100),                                                                                                                                                                                               
        slight_pct  =('collision_severity', lambda x: (x == 3).mean() * 100),
        lat         =('latitude',  'mean'),                                                                                                                                                                                                                                 
        lon         =('longitude', 'mean'),
    )                                                                                                                                                                                                                                                                       
    .sort_values('crash_count', ascending=False)
    .reset_index()                                                                                                                                                                                                                                                          
)
cluster_stats.to_csv(OUT_DIR / 'cluster_stats.csv', index=False)                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                              
print("\n=== TOP 10 CLUSTERS ===")
print(cluster_stats[['cluster','crash_count','fatal_pct','serious_pct','slight_pct']].head(10).to_string(index=False))                                                                                                                                                      
                                                                                                                                                                                                                                                                              
print("\n=== HOTSPOT vs NON-HOTSPOT ===")                                                                                                                                                                                                                                   
for label, grp in [('Hotspot', hotspot), ('Non-hotspot', non_hotspot)]:                                                                                                                                                                                                     
    f  = (grp['collision_severity'] == 1).mean() * 100                                                                                                                                                                                                                      
    s  = (grp['collision_severity'] == 2).mean() * 100                                                                                                                                                                                                                      
    sl = (grp['collision_severity'] == 3).mean() * 100
    print(f"  {label:12s}  Fatal={f:.2f}%  Serious={s:.1f}%  Slight={sl:.1f}%")                                                                                                                                                                                             
                                                                                                                                                                                                                                                                              
# ── MAP 2: Cluster map ────────────────────────────────────────────────────────                                                                                                                                                                                            
print("\nBuilding cluster map...")                                                                                                                                                                                                                                          
m2 = folium.Map(location=uk_centre, zoom_start=6, tiles='CartoDB positron')                                                                                                                                                                                                 
top100    = cluster_stats.head(100)
max_count = top100['crash_count'].max()                                                                                                                                                                                                                                     
   
for _, row in top100.iterrows():                                                                                                                                                                                                                                            
    radius = 6 + 25 * (row['crash_count'] / max_count)
    color  = ('#b71c1c' if row['fatal_pct'] > 3 else
             '#e53935' if row['fatal_pct'] > 1.5 else                                                                                                                                                                                                                      
             '#ef6c00' if row['serious_pct'] > 30 else '#1565c0')                                                                                                                                                                                                          
    folium.CircleMarker(                                                                                                                                                                                                                                                    
        location=[row['lat'], row['lon']],                                                                                                                                                                                                                                  
        radius=radius,                                                                                                                                                                                                                                                      
        color=color, fill=True, fill_color=color, fill_opacity=0.55, weight=1,
        popup=folium.Popup(                                                                                                                                                                                                                                                 
            f"<b>Cluster {int(row['cluster'])}</b><br>"                                                                                                                                                                                                                     
            f"Crashes: {int(row['crash_count']):,}<br>"
            f"Fatal: {row['fatal_pct']:.1f}%<br>"                                                                                                                                                                                                                           
            f"Serious: {row['serious_pct']:.1f}%<br>"                                                                                                                                                                                                                       
            f"Slight: {row['slight_pct']:.1f}%",
            max_width=180                                                                                                                                                                                                                                                   
        )       
    ).add_to(m2)
                                                                                                                                                                                                                                                                              
legend = """<div style="position:fixed;bottom:40px;left:40px;background:white;
            padding:10px;border-radius:6px;font-size:12px;border:1px solid #ccc;z-index:1000">                                                                                                                                                                              
    <b>Hotspot severity</b><br>                                                                                                                                                                                                                                             
    <span style="color:#b71c1c">&#9679;</span> Fatal &gt;3%<br>
    <span style="color:#e53935">&#9679;</span> Fatal 1.5–3%<br>                                                                                                                                                                                                             
    <span style="color:#ef6c00">&#9679;</span> Serious &gt;30%<br>
    <span style="color:#1565c0">&#9679;</span> Mostly slight<br>                                                                                                                                                                                                            
    <i>Size = crash volume</i></div>"""                                                                                                                                                                                                                                     
m2.get_root().html.add_child(folium.Element(legend))
m2.save(OUT_DIR / 'hotspot_clusters.html')                                                                                                                                                                                                                                  
print("  → hotspot_clusters.html")
                                                                                                                                                                                                                                                                              
# ── Static plot ───────────────────────────────────────────────────────────────                                                                                                                                                                                            
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
                                                                                                                                                                                                                                                                              
categories = ['Fatal', 'Serious', 'Slight']
in_vals    = [(hotspot['collision_severity']     == i).mean()*100 for i in [1,2,3]]
out_vals   = [(non_hotspot['collision_severity'] == i).mean()*100 for i in [1,2,3]]                                                                                                                                                                                         
x, w = np.arange(3), 0.35                                                                                                                                                                                                                                                   
b1 = axes[0].bar(x-w/2, in_vals,  w, label='Hotspot',     color=['#c62828','#ef6c00','#2e7d32'])                                                                                                                                                                            
b2 = axes[0].bar(x+w/2, out_vals, w, label='Non-hotspot', color=['#ef9a9a','#ffcc80','#a5d6a7'])                                                                                                                                                                            
axes[0].set_xticks(x); axes[0].set_xticklabels(categories)                                                                                                                                                                                                                  
axes[0].set_ylabel('% of crashes'); axes[0].set_title('Severity: Hotspot vs Non-hotspot')                                                                                                                                                                                   
axes[0].legend()                                                                                                                                                                                                                                                            
for bars in [b1, b2]:
    for bar in bars:                                                                                                                                                                                                                                                        
        h = bar.get_height()
        axes[0].text(bar.get_x()+bar.get_width()/2, h+0.1, f'{h:.1f}%',
                    ha='center', fontsize=8)                                                                                                                                                                                                                               
   
top20 = cluster_stats.head(20)                                                                                                                                                                                                                                              
bar_colors = ['#b71c1c' if f>3 else '#e53935' if f>1.5 else '#ef6c00' if s>30 else '#1565c0'
            for f,s in zip(top20['fatal_pct'], top20['serious_pct'])]                                                                                                                                                                                                     
axes[1].barh(range(20), top20['crash_count'][::-1].values, color=bar_colors[::-1])
axes[1].set_yticks(range(20))                                                                                                                                                                                                                                               
axes[1].set_yticklabels([f"#{int(c)}  ({int(n):,})" for c,n in
                        zip(top20['cluster'][::-1], top20['crash_count'][::-1])], fontsize=8)                                                                                                                                                                             
axes[1].set_xlabel('Crash count'); axes[1].set_title('Top 20 Clusters by Volume')                                                                                                                                                                                           
   
plt.suptitle('STATS19 Spatial Hotspot Analysis (2020–2024)', fontsize=13, fontweight='bold')                                                                                                                                                                                
plt.tight_layout()
plt.savefig(OUT_DIR / 'spatial_analysis.png', dpi=150, bbox_inches='tight')                                                                                                                                                                                                 
plt.close()     
print("  → spatial_analysis.png")
print(f"\nDone. All outputs in {OUT_DIR}/")                                                                                                                                                                                                                                 