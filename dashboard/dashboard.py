import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set page configuration
st.set_page_config(
    page_title="Capital Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }
    
    .card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .card-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 0.25rem;
    }
    
    .card-desc {
        font-size: 0.813rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data helper with cache to prevent reload delay
@st.cache_data
def load_data():
    # Load dari folder dashboard
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(data_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data dari {e}. Silakan periksa apakah 'dashboard/main_data.csv' sudah ada.")
    st.stop()

# ==========================================
# MAIN CONTENT HEADER
# ==========================================

st.markdown("<div class='main-title'>Capital Bike Sharing Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Visualisasi interaktif performa operasional penyewaan sepeda berdasarkan data historis 2011-2012</div>", unsafe_allow_html=True)

# ==========================================
# DATASET ASSIGNMENT (NO FILTERS)
# ==========================================

filtered_df = df

# Calculations for metrics
total_rentals = filtered_df['cnt'].sum()
total_registered = filtered_df['registered'].sum()
total_casual = filtered_df['casual'].sum()

reg_ratio = (total_registered / total_rentals) * 100 if total_rentals > 0 else 0
cas_ratio = (total_casual / total_rentals) * 100 if total_rentals > 0 else 0

# Metric Cards using Columns with HTML markup for premium styling
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='card' style='border-left: 5px solid #3b82f6;'>
        <div class='card-title'>Total Penyewaan</div>
        <div class='card-value'>{total_rentals:,}</div>
        <div class='card-desc'>Total peminjaman sepeda pada periode terpilih</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='card' style='border-left: 5px solid #10b981;'>
        <div class='card-title'>Pengguna Terdaftar (Registered)</div>
        <div class='card-value'>{total_registered:,}</div>
        <div class='card-desc'>{reg_ratio:.1f}% dari total penyewaan</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card' style='border-left: 5px solid #f59e0b;'>
        <div class='card-title'>Pengguna Kasual (Casual)</div>
        <div class='card-value'>{total_casual:,}</div>
        <div class='card-desc'>{cas_ratio:.1f}% dari total penyewaan</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# VISUALISASI UTAMA (SIDE-BY-SIDE / GRID LAYOUT)
# ==========================================

st.markdown("### Tren Perkembangan & Kinerja Bulanan")

# 1. Monthly Trend Analysis
monthly_data = filtered_df.groupby(['year_label', 'mnth']).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
}).reset_index()

monthly_data['year_month'] = monthly_data['year_label'].astype(str) + '-' + monthly_data['mnth'].astype(str).str.zfill(2)

col_plot1, col_info1 = st.columns([3, 1])

with col_plot1:
    fig1, ax1 = plt.subplots(figsize=(12, 5.5))
    ax1.plot(monthly_data['year_month'], monthly_data['casual'], marker='o', color='#f59e0b', label='Casual Users', linewidth=2.5)
    ax1.plot(monthly_data['year_month'], monthly_data['registered'], marker='o', color='#10b981', label='Registered Users', linewidth=2.5)
    ax1.plot(monthly_data['year_month'], monthly_data['cnt'], marker='o', color='#3b82f6', label='Total Rentals', linewidth=2.5, linestyle='--')
    
    ax1.set_title("Pertumbuhan Penyewaan Sepeda Bulanan (2011-2012)", fontsize=13, fontweight='bold', pad=12)
    ax1.set_xlabel("Bulan (Tahun-Bulan)", fontsize=10)
    ax1.set_ylabel("Jumlah Penyewaan (Units)", fontsize=10)
    plt.xticks(rotation=45)
    ax1.legend(frameon=True, facecolor='white', edgecolor='none')
    ax1.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig1)
    
with col_info1:
    st.markdown("""
    **Tren Bulanan:**
    - **Pertumbuhan Cepat:** Terjadi peningkatan peminjaman yang masif dari tahun 2011 ke 2012.
    - **Dominasi Terdaftar:** Pengguna terdaftar (*Registered*) mendominasi lebih dari 75% total transaksi.
    - **Pola Musiman:** Permintaan sewa memuncak di pertengahan tahun dan menurun tajam di akhir/awal tahun.
    """)

st.markdown("---")
st.markdown("### Analisis Pola Waktu & Musiman")

col_left2, col_right2 = st.columns(2)

with col_left2:
    # 2. Hourly patterns
    hourly_data = filtered_df.groupby(['workingday', 'hr'])['cnt'].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.lineplot(
        data=hourly_data,
        x='hr',
        y='cnt',
        hue='workingday',
        marker='o',
        palette={0: '#ef4444', 1: '#2563eb'},
        linewidth=2.5,
        errorbar=None,
        ax=ax2
    )
    ax2.set_title("Pola Rata-rata Penyewaan per Jam: Hari Kerja vs Hari Libur", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Jam (Hour)")
    ax2.set_ylabel("Rata-rata Penyewaan (Units)")
    ax2.set_xticks(range(0, 24, 2))
    ax2.legend(title='Tipe Hari', labels=['Hari Libur / Weekend', 'Hari Kerja'], loc='upper left')
    ax2.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig2)
    st.markdown("""
    * **Hari Kerja:** Pola *bimodal* dengan dua puncak tajam pada jam berangkat kerja (**08:00**) dan jam pulang kerja (**17:00 - 18:00**).
    * **Hari Libur:** Pola *unimodal* di mana permintaan memuncak di siang hingga sore hari (**12:00 - 16:00**).
    """)

with col_right2:
    # 3. Season patterns
    season_agg = filtered_df.groupby('season_label').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    }).reindex(['Spring', 'Summer', 'Fall', 'Winter']).reset_index()
    
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(season_agg['season_label']))
    width = 0.35
    
    ax3.bar(x - width/2, season_agg['casual'], width, label='Casual', color='#f59e0b')
    ax3.bar(x + width/2, season_agg['registered'], width, label='Registered', color='#10b981')
    
    ax3.set_title("Rata-rata Penyewaan Harian berdasarkan Musim", fontsize=12, fontweight='bold')
    ax3.set_xlabel("Musim (Season)")
    ax3.set_ylabel("Rata-rata Penyewaan Harian (Units)")
    ax3.set_xticks(x)
    ax3.set_xticklabels(season_agg['season_label'])
    ax3.legend()
    ax3.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig3)
    st.markdown("""
    * **Musim Terpopuler:** Musim Gugur (*Fall*) dan Musim Panas (*Summer*) memiliki rata-rata penyewaan tertinggi.
    * **Musim Terendah:** Musim Semi (*Spring*) mencatat permintaan paling rendah karena cuaca transisi yang dingin.
    """)

st.markdown("---")
st.markdown("### Analisis Cuaca & Klaster Permintaan (Lanjutan)")

# Aggregating daily data for clustering
daily_df = filtered_df.groupby('dteday').agg({
    'cnt': 'sum',
    'temp_celcius': 'mean',
    'humidity_pct': 'mean',
    'windspeed_kmh': 'mean',
    'weather_label': lambda x: x.mode()[0] if not x.mode().empty else 'Unknown',
    'season_label': lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
}).reset_index()

def classify_demand(cnt):
    if cnt < 3000:
        return 'Low Demand'
    elif cnt <= 6000:
        return 'Medium Demand'
    else:
        return 'High Demand'
        
daily_df['demand_cluster'] = daily_df['cnt'].apply(classify_demand)
daily_df['demand_cluster'] = pd.Categorical(daily_df['demand_cluster'], categories=['Low Demand', 'Medium Demand', 'High Demand'], ordered=True)

cluster_summary = daily_df.groupby('demand_cluster', observed=False).agg({
    'temp_celcius': 'mean',
    'humidity_pct': 'mean',
    'windspeed_kmh': 'mean',
    'cnt': ['mean', 'count']
}).reset_index()

cluster_summary.columns = ['Demand Cluster', 'Mean Temp (C)', 'Mean Humidity (%)', 'Mean Windspeed (km/h)', 'Mean Rentals', 'Count (Days)']

col_left3, col_right3 = st.columns(2)

with col_left3:
    # 4. Weather patterns
    weather_agg = filtered_df.groupby('weather_label').agg({
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    }).reset_index().sort_values(by='cnt', ascending=False)
    
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=weather_agg,
        x='weather_label',
        y='cnt',
        hue='weather_label',
        palette='Blues_r',
        legend=False,
        ax=ax4
    )
    ax4.set_title("Rata-rata Penyewaan berdasarkan Kondisi Cuaca", fontsize=12, fontweight='bold')
    ax4.set_xlabel("Kondisi Cuaca")
    ax4.set_ylabel("Rata-rata Penyewaan (Units)")
    ax4.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig4)
    st.markdown("""
    * **Kondisi Cerah:** Rata-rata penyewaan tertinggi terjadi saat cuaca cerah/berawan tipis (*Clear*).
    * **Cuaca Buruk:** Penurunan sangat drastis terjadi pada kondisi hujan/salju lebat.
    """)

with col_right3:
    # 5. Temperature distribution by cluster
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    sns.boxplot(
        data=daily_df,
        x='demand_cluster',
        y='temp_celcius',
        palette=['#f87171', '#fbbf24', '#34d399'],
        ax=ax5
    )
    ax5.set_title("Distribusi Suhu untuk Setiap Klaster Permintaan", fontsize=12, fontweight='bold')
    ax5.set_xlabel("Klaster Permintaan (Demand Cluster)")
    ax5.set_ylabel("Suhu (°C)")
    ax5.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig5)
    st.markdown("""
    * **High Demand:** Rata-rata suhu berada pada tingkat hangat yang nyaman (~23.3°C).
    * **Low Demand:** Rata-rata suhu berkisar pada suhu dingin (~11.6°C).
    """)

# Summary table for clusters
st.markdown("#### Karakteristik Cuaca per Klaster Permintaan (Manual Clustering)", unsafe_allow_html=True)
col_tbl, col_tbl_info = st.columns([2, 3])

with col_tbl:
    st.dataframe(cluster_summary.style.format({
        'Mean Temp (C)': '{:.1f}°C',
        'Mean Humidity (%)': '{:.1f}%',
        'Mean Windspeed (km/h)': '{:.1f} km/h',
        'Mean Rentals': '{:,.0f}',
        'Count (Days)': '{:,.0f}'
    }))

with col_tbl_info:
    st.markdown("""
    **Analisis Klaster Permintaan Harian:**
    - Hari dengan tingkat permintaan tinggi (**High Demand**) memiliki suhu hangat rata-rata yang optimal serta kelembapan yang seimbang (~59%).
    - Hari dengan tingkat permintaan rendah (**Low Demand**) didominasi oleh suhu dingin rata-rata (~11°C) yang tidak ramah bagi pesepeda luar ruangan.
    """)

# Footer
st.markdown("<br><hr><div style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>Capital Bike Sharing Dashboard</div>", unsafe_allow_html=True)
