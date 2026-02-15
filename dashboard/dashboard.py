import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Dashboard - Vania Rachmawati Dewi",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    df_day = pd.read_csv('clean_bike_rental_day.csv')
    df_day['dateday'] = pd.to_datetime(df_day['dateday'])
    return df_day

df = load_data()

# Sidebar - Profil dan Filter
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2972/2972185.png", width=150)
    st.markdown("# 🚲 Bike Sharing Dashboard")
    st.markdown("---")
    
    st.markdown("### 👤 Profil")
    st.markdown("**Nama:** Vania Rachmawati Dewi")
    st.markdown("**Email:** vaniardewi@gmail.com")
    st.markdown("**ID Dicoding:** vaniard")
    
    st.markdown("---")
    st.markdown("### 🎯 Filter Data")
    
    # Filter Tahun
    years = df['year'].unique()
    selected_years = st.multiselect(
        "Tahun",
        options=sorted(years),
        default=sorted(years)
    )
    
    # Filter Musim
    seasons = df['season'].unique()
    season_names = {
        'spring': 'Spring', 
        'summer': 'Summer', 
        'fall': 'Fall', 
        'winter': 'Winter'
    }
    selected_seasons = st.multiselect(
        "Musim",
        options=seasons,
        format_func=lambda x: season_names.get(x, x),
        default=seasons
    )
    
    # Filter Cuaca
    weather = df['weather_condition'].unique()
    weather_names = {
        'clear': 'Clear',
        'mist': 'Mist',
        'light rain': 'Light Rain',
        'heavy rain': 'Heavy Rain'
    }
    selected_weather = st.multiselect(
        "Kondisi Cuaca",
        options=weather,
        format_func=lambda x: weather_names.get(x, x),
        default=weather
    )
    
    # Filter Hari
    day_type = st.radio(
        "Tipe Hari",
        options=['Semua', 'Weekday', 'Weekend']
    )
    
    st.markdown("---")
    st.markdown("### 📊 Tentang Dataset")
    st.markdown(f"""
    - **Total Data:** {len(df)} hari
    - **Periode:** {df['dateday'].min().strftime('%d %b %Y')} - {df['dateday'].max().strftime('%d %b %Y')}
    - **Rata-rata Penyewaan:** {df['count'].mean():.0f}/hari
    """)

# Apply filter
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['season'].isin(selected_seasons)) &
    (df['weather_condition'].isin(selected_weather))
]

if day_type == 'Weekday':
    filtered_df = filtered_df[filtered_df['day_type'] == 'weekday']
elif day_type == 'Weekend':
    filtered_df = filtered_df[filtered_df['day_type'] == 'weekend']

# Header
st.title("🚴‍♂️ Proyek Analisis Data: Bike Sharing")
st.markdown("---")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📅 Total Hari", f"{len(filtered_df):,}")
with col2:
    st.metric("🚲 Total Penyewaan", f"{filtered_df['count'].sum():,}")
with col3:
    st.metric("📊 Rata-rata/Hari", f"{filtered_df['count'].mean():.0f}")
with col4:
    st.metric("🏆 Penyewaan Tertinggi", f"{filtered_df['count'].max():,}")

st.markdown("---")

# ============================================================================
# VISUALISASI 1: Rata-rata Penyewaan per Bulan (Barplot)
# ============================================================================
st.header("📊 Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Rata-rata Penyewaan per Bulan")
    
    # Persiapan data - SESUAI DENGAN NOTEBOOK
    month_names_id = {
        'january': 'Jan', 'february': 'Feb', 'march': 'Mar', 'april': 'Apr',
        'may': 'Mei', 'june': 'Jun', 'july': 'Jul', 'august': 'Aug',
        'september': 'Sep', 'october': 'Oct', 'november': 'Nov', 'december': 'Dec'
    }
    
    month_avg = filtered_df.groupby('month')['count'].mean().reset_index()
    month_order = ['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']
    month_avg['month'] = pd.Categorical(month_avg['month'], categories=month_order, ordered=True)
    month_avg = month_avg.sort_values('month')
    month_avg['month_display'] = month_avg['month'].map(month_names_id)
    
    # Membuat barplot dengan matplotlib - SESUAI NOTEBOOK
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, 12))
    bars = ax.bar(month_avg['month_display'], month_avg['count'], color=colors)
    
    ax.set_title('Rata-rata Jumlah Penyewaan Sepeda Berdasarkan Bulan', fontsize=14, pad=20)
    ax.set_xlabel('Bulan', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    # Tambahkan nilai di atas bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📊 Statistik Penyewaan per Bulan")
    
    # Tabel statistik - SESUAI NOTEBOOK
    month_stats = filtered_df.groupby(by='month').agg({
        'count': ['max', 'min', 'mean', 'sum']
    }).round(2)
    
    month_stats.columns = ['Max', 'Min', 'Rata-rata', 'Total']
    month_stats.index = month_stats.index.map(lambda x: month_names_id.get(x, x))
    month_stats = month_stats.reindex([month_names_id[m] for m in month_order])
    
    st.dataframe(
        month_stats.style.background_gradient(cmap='Blues', subset=['Rata-rata', 'Total']),
        width='stretch'
    )
    
    st.info("""
    **Insight:**
    - Bulan September dan Juni memiliki rata-rata penyewaan tertinggi (5.766 dan 5.772)
    - Bulan Januari memiliki rata-rata penyewaan terendah
    - Musim panas dan awal musim gugur adalah periode puncak penyewaan
    """)

# ============================================================================
# VISUALISASI 2: Distribusi Penyewaan per Musim (Boxplot)
# ============================================================================
st.subheader("📦 Distribusi Jumlah Penyewaan Sepeda Berdasarkan Musim")

col1, col2 = st.columns([2, 1])

with col1:
    # Boxplot - SESUAI NOTEBOOK
    fig, ax = plt.subplots(figsize=(10, 6))
    
    season_order = ['spring', 'summer', 'fall', 'winter']
    season_names_id = {'spring': 'Spring', 'summer': 'Summer', 'fall': 'Fall', 'winter': 'Winter'}
    
    # Siapkan data untuk boxplot
    plot_data = filtered_df.copy()
    plot_data['season_display'] = pd.Categorical(
        plot_data['season'], 
        categories=season_order, 
        ordered=True
    )
    plot_data['season_display'] = plot_data['season_display'].map(season_names_id)
    
    sns.boxplot(x='season_display', y='count', data=plot_data, 
                palette='viridis', ax=ax)
    
    ax.set_title('Distribusi Jumlah Penyewaan Sepeda Berdasarkan Musim', fontsize=14, pad=20)
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # Statistik per musim
    season_stats = filtered_df.groupby('season').agg({
        'casual': 'mean',
        'registered': 'mean',
        'count': ['mean', 'min', 'max']
    }).round(2)
    
    season_stats.columns = ['Casual', 'Registered', 'Rata-rata', 'Min', 'Max']
    season_stats = season_stats.reindex(season_order)
    season_stats.index = [season_names_id[s] for s in season_order]
    
    st.dataframe(season_stats, width='stretch')
    
    st.info("""
    **Insight:**
    - **Musim Gugur (Fall)** memiliki rata-rata tertinggi (5.644)
    - **Musim Semi (Spring)** memiliki rata-rata terendah (2.604)
    - **Musim Dingin (Winter)** menunjukkan variasi terbesar
    """)

st.markdown("---")

# ============================================================================
# VISUALISASI 3: Analisis Cuaca
# ============================================================================
st.header("☁️ Pengaruh Cuaca terhadap Pengguna Sepeda")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌤️ Rata-rata Penyewaan per Kondisi Cuaca")
    
    # Barplot cuaca - SESUAI NOTEBOOK
    weather_avg = filtered_df.groupby('weather_condition')['count'].mean().reset_index()
    weather_names_id = {'clear': 'Clear', 'mist': 'Mist', 'light rain': 'Lighr Rain'}
    weather_avg['weather_display'] = weather_avg['weather_condition'].map(weather_names_id)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(weather_avg)))
    bars = ax.bar(weather_avg['weather_display'], weather_avg['count'], color=colors)
    
    ax.set_title('Rata-rata Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca', 
                fontsize=14, pad=20)
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("👥 Casual vs Registered per Kondisi Cuaca")
    
    # Barplot casual vs registered - SESUAI NOTEBOOK
    weather_user = filtered_df.groupby('weather_condition')[['casual', 'registered']].mean().reset_index()
    weather_user['weather_display'] = weather_user['weather_condition'].map(weather_names_id)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(weather_user))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, weather_user['casual'], width, 
                   label='Casual', color='skyblue', edgecolor='black', linewidth=0.5)
    bars2 = ax.bar(x + width/2, weather_user['registered'], width, 
                   label='Registered', color='teal', edgecolor='black', linewidth=0.5)
    
    ax.set_title('Rata-rata Jumlah Penyewaan Sepeda (Casual vs Registered) Berdasarkan Kondisi Cuaca',
                fontsize=14, pad=20)
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(weather_user['weather_display'])
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Tabel statistik cuaca
st.subheader("📋 Statistik Penyewaan per Kondisi Cuaca")

weather_stats = filtered_df.groupby(by='weather_condition').agg({
    'count': ['max', 'min', 'mean', 'sum'],
    'casual': 'mean',
    'registered': 'mean'
}).round(2)

weather_stats.columns = ['Max', 'Min', 'Rata-rata', 'Total', 'Rata-rata Casual', 'Rata-rata Registered']
weather_stats.index = weather_stats.index.map(lambda x: weather_names_id.get(x, x))

st.dataframe(weather_stats.style.background_gradient(cmap='YlOrRd', subset=['Rata-rata', 'Total']),
            width='stretch')

st.success("""
**Kesimpulan Analisis Cuaca:**
- **Cuaca Cerah (Clear)** merupakan kondisi paling ideal dengan rata-rata penyewaan tertinggi
- **Cuaca Berkabut (Mist)** masih menarik penyewa, terutama pengguna registered yang lebih stabil
- **Hujan Ringan (Light Rain)** sangat menghambat aktivitas penyewaan, penurunan drastis pada kedua tipe pengguna
""")

st.markdown("---")

# ============================================================================
# VISUALISASI 4: Analisis Hari Kerja vs Akhir Pekan
# ============================================================================
st.header("📅 Analisis Hari Kerja vs Akhir Pekan")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Weekday vs Weekend")
    
    # Barplot weekday vs weekend - SESUAI NOTEBOOK
    day_type_avg = filtered_df.groupby('day_type')['count'].mean().reset_index()
    day_type_names = {'weekday': 'Weekday', 'weekend': 'Weekend'}
    day_type_avg['day_display'] = day_type_avg['day_type'].map(day_type_names)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#FF6B6B', '#4ECDC4']
    bars = ax.bar(day_type_avg['day_display'], day_type_avg['count'], color=colors, 
                  edgecolor='black', linewidth=0.5)
    
    ax.set_title('Rata-rata Jumlah Penyewaan Sepeda: Hari Kerja vs Akhir Pekan',
                fontsize=14, pad=20)
    ax.set_xlabel('Tipe Hari', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 20,
                f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📆 Rata-rata Penyewaan per Hari")
    
    # Barplot per hari - SESUAI NOTEBOOK
    day_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_names_id = {
        'monday': 'Monday', 'tuesday': 'Tuesday', 'wednesday': 'Wednesday', 
        'thursday': 'Thursday', 'friday': 'Friday', 'saturday': 'Saturday', 'sunday': 'Monday'
    }
    
    weekday_avg = filtered_df.groupby('weekday')['count'].mean().reset_index()
    weekday_avg['weekday'] = pd.Categorical(weekday_avg['weekday'], categories=day_order, ordered=True)
    weekday_avg = weekday_avg.sort_values('weekday')
    weekday_avg['day_display'] = weekday_avg['weekday'].map(day_names_id)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Paired(np.linspace(0.1, 0.9, 7))
    bars = ax.bar(weekday_avg['day_display'], weekday_avg['count'], color=colors,
                  edgecolor='black', linewidth=0.5)
    
    ax.set_title('Rata-rata Jumlah Penyewaan Sepeda per Hari', fontsize=14, pad=20)
    ax.set_xlabel('Hari', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Penyewaan', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================================
# VISUALISASI 5: RFM Analysis
# ============================================================================
st.header("🎯 RFM Analysis - Segmentasi Hari")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Distribusi Segmen RFM")
    
    # Barplot RFM segments - SESUAI NOTEBOOK
    segment_counts = filtered_df['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Jumlah']
    
    segment_order = ['Best Days', 'Good Days', 'Regular Days', 'Needs Attention', 'Lost Days']
    segment_counts['Segment'] = pd.Categorical(segment_counts['Segment'], 
                                              categories=segment_order, ordered=True)
    segment_counts = segment_counts.sort_values('Segment')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(segment_counts)))
    bars = ax.bar(segment_counts['Segment'], segment_counts['Jumlah'], color=colors,
                  edgecolor='black', linewidth=0.5)
    
    ax.set_title('Distribusi Hari di Seluruh Segmen RFM', fontsize=14, pad=20)
    ax.set_xlabel('Segmen RFM', fontsize=12)
    ax.set_ylabel('Jumlah Hari', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("📋 Detail Segmen RFM")
    
    rfm_summary = filtered_df.groupby('Segment').agg({
        'count': ['mean', 'min', 'max'],
        'Recency': 'mean',
        'R_Score': 'mean',
        'F_Score': 'mean',
        'M_Score': 'mean'
    }).round(2)
    
    rfm_summary.columns = ['Rata-rata', 'Min', 'Max', 'Recency', 'R', 'F', 'M']
    rfm_summary = rfm_summary.reindex(segment_order)
    
    st.dataframe(
        rfm_summary.style.background_gradient(cmap='Blues', subset=['Rata-rata', 'Recency']),
        width='stretch'
    )

st.info("""
**Insight RFM Analysis:**
- **Best Days (249 hari)**: Hari-hari terbaik dengan penyewaan tertinggi dan recency terbaru
- **Regular Days (231 hari)**: Hari-hari dengan performa rata-rata
- **Lost Days (172 hari)**: Hari-hari dengan penyewaan rendah dan sudah lama berlalu
- **Good Days (53 hari)**: Hari-hari baik namun tidak sebaik Best Days
- **Needs Attention (26 hari)**: Hari-hari yang perlu perhatian khusus
""")

st.markdown("---")

# ============================================================================
# VISUALISASI 6: Clustering & Kategorisasi
# ============================================================================
st.header("📈 Clustering & Kategorisasi")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌡️ Kategori Suhu")
    
    # Countplot kategori suhu - SESUAI NOTEBOOK
    temp_counts = filtered_df['temp_category'].value_counts().reset_index()
    temp_counts.columns = ['Kategori', 'Jumlah']
    
    temp_order = ['Cold', 'Mild', 'Warm', 'Hot']
    temp_names = {'Cold': 'Cold', 'Mild': 'Mild', 'Warm': 'Warm', 'Hot': 'Hot'}
    
    temp_counts['Kategori'] = pd.Categorical(temp_counts['Kategori'], categories=temp_order, ordered=True)
    temp_counts = temp_counts.sort_values('Kategori')
    temp_counts['display'] = temp_counts['Kategori'].map(temp_names)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#ADD8E6', '#90EE90', '#FFD700', '#FFA07A']
    bars = ax.bar(temp_counts['display'], temp_counts['Jumlah'], color=colors,
                  edgecolor='black', linewidth=0.5)
    
    ax.set_title('Distribusi Hari Berdasarkan Kategori Suhu', fontsize=12, pad=15)
    ax.set_xlabel('Kategori Suhu', fontsize=10)
    ax.set_ylabel('Jumlah Hari', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("💧 Kategori Kelembaban")
    
    # Countplot kategori kelembaban - SESUAI NOTEBOOK
    hum_counts = filtered_df['hum_category'].value_counts().reset_index()
    hum_counts.columns = ['Kategori', 'Jumlah']
    
    hum_order = ['Low Humidity', 'Medium Humidity', 'High Humidity']
    hum_names = {'Low Humidity': 'Low Humidity', 'Medium Humidity': 'Medium Humidity', 'High Humidity': 'High Humidity'}
    
    hum_counts['Kategori'] = pd.Categorical(hum_counts['Kategori'], categories=hum_order, ordered=True)
    hum_counts = hum_counts.sort_values('Kategori')
    hum_counts['display'] = hum_counts['Kategori'].map(hum_names)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ['#87CEEB', '#4682B4', '#2E5984']
    bars = ax.bar(hum_counts['display'], hum_counts['Jumlah'], color=colors,
                  edgecolor='black', linewidth=0.5)
    
    ax.set_title('Distribusi Hari Berdasarkan Kategori Kelembaban', fontsize=12, pad=15)
    ax.set_xlabel('Kategori Kelembaban', fontsize=10)
    ax.set_ylabel('Jumlah Hari', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col3:
    st.subheader("📊 Kategori Volume Penyewaan")
    
    # Countplot kategori volume - SESUAI NOTEBOOK
    rental_counts = filtered_df['rental_volume_category'].value_counts().reset_index()
    rental_counts.columns = ['Kategori', 'Jumlah']
    
    rental_order = ['Low Rentals', 'Medium Rentals', 'High Rentals', 'Very High Rentals']
    rental_names = {
        'Low Rentals': 'Rendah', 
        'Medium Rentals': 'Sedang', 
        'High Rentals': 'Tinggi', 
        'Very High Rentals': 'Sangat Tinggi'
    }
    
    rental_counts['Kategori'] = pd.Categorical(rental_counts['Kategori'], categories=rental_order, ordered=True)
    rental_counts = rental_counts.sort_values('Kategori')
    rental_counts['display'] = rental_counts['Kategori'].map(rental_names)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, 4))
    bars = ax.bar(rental_counts['display'], rental_counts['Jumlah'], color=colors,
                  edgecolor='black', linewidth=0.5)
    
    ax.set_title('Distribusi Hari Berdasarkan Kategori Volume Penyewaan', fontsize=12, pad=15)
    ax.set_xlabel('Kategori Volume', fontsize=10)
    ax.set_ylabel('Jumlah Hari', fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

st.markdown("---")

# ============================================================================
# KESIMPULAN
# ============================================================================
st.header("📝 Conclusion")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍂 Pengaruh Musim terhadap Penyewaan")
    st.markdown("""
    - **Musim Gugur (Fall)** dan **Musim Panas (Summer)** merupakan periode puncak penyewaan sepeda
    - Sebagian besar hari di musim ini memiliki volume penyewaan yang sangat banyak
    - **Musim Dingin (Winter)** menunjukkan distribusi penyewaan yang lebih luas, dengan variasi tinggi-rendah
    - **Musim Semi (Spring)** merupakan musim dengan aktivitas penyewaan sepeda terendah
    """)

with col2:
    st.subheader("☁️ Pengaruh Cuaca terhadap Pengguna")
    st.markdown("""
    - **Cuaca Cerah (Clear)** merupakan kondisi paling ideal dengan rata-rata penyewaan tertinggi
    - **Cuaca Berkabut (Mist)** masih menarik penyewa, pengguna registered lebih stabil
    - **Hujan Ringan (Light Rain)** sangat menghambat aktivitas penyewaan
    - Pengguna **registered** cenderung lebih stabil dibandingkan pengguna **casual**
    """)

st.success("""
**Kesimpulan Utama:**
Pola penyewaan sepeda sangat dipengaruhi oleh faktor musiman dan kondisi cuaca. 
Musim gugur dan musim panas, serta cuaca cerah adalah pendorong utama peningkatan penggunaan sepeda. 
Akhir pekan juga menunjukkan permintaan yang lebih tinggi untuk tujuan rekreasi.
""")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px; background-color: #f5f5f5; border-radius: 10px;'>
    <h4>🚲 Dashboard Analisis Bike Sharing</h4>
    <p><strong>Nama:</strong> Vania Rachmawati Dewi | <strong>Email:</strong> vaniardewi@gmail.com | <strong>ID Dicoding:</strong> vaniard</p>
    <p>© 2026 - Proyek Analisis Data</p>
</div>
""", unsafe_allow_html=True)

# Tambahkan CSS kustom
st.markdown("""
<style>
    .stApp {
        background-color: #fafafa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)