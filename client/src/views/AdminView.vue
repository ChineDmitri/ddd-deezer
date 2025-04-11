<template>
  <div class="admin-container">
    <h1>Espace Direction</h1>
    
    <div class="admin-actions">
      <button class="admin-console-btn" @click="openAdminConsole">
        <span class="admin-console-icon">⚙️</span>
        System Admin Console
      </button>
      
      <router-link to="/map" class="map-link-btn">
        <span class="map-icon">🗺️</span>
        Voir la carte des tendances
      </router-link>
    </div>
    
    <div class="dashboard-grid">
      <!-- Server Status -->
      <div class="status-card">
        <h2>Server Status</h2>
        <div class="server-status">
          <span :class="['status-indicator', serverStatus ? 'online' : 'offline']"></span>
          <span>{{ serverStatus ? 'Online' : 'Offline' }}</span>
        </div>
      </div>

      <!-- User Statistics -->
      <div class="stats-card">
        <h2>User Statistics</h2>
        <div v-if="loading">Loading statistics...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else class="stats-grid">
          <div class="stat-item">
            <div class="stat-value">{{ userStats.total_users }}</div>
            <div class="stat-label">Total Users</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ userStats.total_artists }}</div>
            <div class="stat-label">Artists</div>
            <div class="stat-percentage">{{ userStats.artist_percentage }}%</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ userStats.total_listeners }}</div>
            <div class="stat-label">Listeners</div>
            <div class="stat-percentage">{{ userStats.listener_percentage }}%</div>
          </div>
        </div>
      </div>

      <!-- User Growth Chart -->
      <div class="chart-card">
        <h2>User Growth</h2>
        <div v-if="loadingGrowth">Loading chart data...</div>
        <div v-else-if="errorGrowth" class="error">{{ errorGrowth }}</div>
        <div v-else class="chart-container">
          <canvas ref="growthChart"></canvas>
        </div>
      </div>
    </div>
    
    <!-- Aperçu des genres populaires -->
    <div class="popular-genres-section" v-if="topGenres.length > 0">
      <h2>Top Genres Populaires - Global</h2>
      <div class="genres-grid">
        <div v-for="(genre, index) in topGenres" :key="index" class="genre-card">
          <h4>{{ genre.genre }}</h4>
          <div class="score">{{ genre.score }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';
import { getAccessToken, getRoleBasedApiUrl } from '@/services/authService';
import { useRouter } from 'vue-router';

const router = useRouter();

// References
const growthChart = ref(null);
const loading = ref(true);
const loadingGrowth = ref(true);
const loadingGenres = ref(true);
const error = ref(null);
const errorGrowth = ref(null);
const errorGenres = ref(null);
const serverStatus = ref(false);
const userStats = ref({
  total_users: 0,
  total_artists: 0,
  total_listeners: 0,
  artist_percentage: 0,
  listener_percentage: 0
});
const userGrowth = ref({
  period: '',
  growth_data: []
});
const topGenres = ref([]);

// Open Django Admin Console in a new tab
const openAdminConsole = () => {
  window.open('http://127.0.0.1:8000/admin/', '_blank');
};

// Navigate to map view
const goToMapView = () => {
  router.push('/map');
};

// Check server status
const checkServerStatus = async () => {
  try {
    const token = getAccessToken();
    const response = await fetch('http://127.0.0.1:8000/admin/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    serverStatus.value = response.ok;
  } catch (err) {
    serverStatus.value = false;
  }
};

// Fetch user statistics
const fetchUserStats = async () => {
  loading.value = true;
  try {
    const token = getAccessToken();
    const response = await fetch('http://127.0.0.1:8000/api/auth/user-statistics', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    userStats.value = await response.json();
  } catch (err) {
    error.value = `Failed to load user statistics: ${err.message}`;
  } finally {
    loading.value = false;
  }
};

// Fetch user growth data
const fetchUserGrowth = async () => {
  loadingGrowth.value = true;
  try {
    const token = getAccessToken();
    const response = await fetch('http://127.0.0.1:8000/api/auth/user-growth-statistics/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log("Received growth data:", data);
    
    // Validate data structure and handle empty data
    if (!data.growth_data || data.growth_data.length === 0) {
      console.warn("No growth data received, using mock data for testing");
      userGrowth.value = {
        period: 'month',
        growth_data: [
          { period: '2025-01-01T00:00:00Z', user_count: 2 },
          { period: '2025-02-01T00:00:00Z', user_count: 3 },
          { period: '2025-03-01T00:00:00Z', user_count: 4 },
          { period: '2025-04-01T00:00:00Z', user_count: 5 }
        ]
      };
    } else {
      userGrowth.value = data;
    }
    
    // Use nextTick to ensure DOM is updated before rendering chart
    setTimeout(() => {
      renderGrowthChart();
    }, 0);
  } catch (err) {
    console.error("Error fetching growth data:", err);
    errorGrowth.value = `Failed to load growth data: ${err.message}`;
  } finally {
    loadingGrowth.value = false;
  }
};

// Fetch top genres (similar to listener functionality)
const fetchTopGenres = async () => {
  loadingGenres.value = true;
  try {
    const token = getAccessToken();
    const apiUrl = getRoleBasedApiUrl('popular-genres');
    
    const response = await fetch(apiUrl, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    topGenres.value = data.genres.slice(0, 8); // Limit to top 8 genres
  } catch (err) {
    console.error("Error fetching top genres:", err);
    errorGenres.value = `Failed to load popular genres: ${err.message}`;
  } finally {
    loadingGenres.value = false;
  }
};

// Render growth chart
const renderGrowthChart = () => {
  if (!growthChart.value || userGrowth.value.growth_data.length === 0) return;

  const ctx = growthChart.value.getContext('2d');
  
  // Format dates and extract counts
  const labels = userGrowth.value.growth_data.map(item => {
    const date = new Date(item.period);
    return `${date.toLocaleString('default', { month: 'short' })} ${date.getFullYear()}`;
  });
  
  const data = userGrowth.value.growth_data.map(item => item.user_count);

  // Destroy previous chart instance if it exists
  if (growthChart.value.chart) {
    growthChart.value.chart.destroy();
  }

  // Create new chart instance and store reference directly on the DOM element
  growthChart.value.chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total Users',
        data: data,
        backgroundColor: 'rgba(29, 185, 84, 0.2)',
        borderColor: 'rgba(29, 185, 84, 1)',
        borderWidth: 3,
        tension: 0.4,
        pointBackgroundColor: 'rgba(29, 185, 84, 1)',
        pointRadius: 5,
        pointHoverRadius: 7,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0,
            font: {
              weight: 'bold'
            }
          },
          grid: {
            color: 'rgba(200, 200, 200, 0.2)'
          },
          title: {
            display: true,
            text: 'Number of Users',
            font: {
              weight: 'bold',
              size: 14
            }
          }
        },
        x: {
          grid: {
            color: 'rgba(200, 200, 200, 0.2)'
          },
          ticks: {
            font: {
              weight: 'bold'
            }
          },
          title: {
            display: true,
            text: 'Period',
            font: {
              weight: 'bold',
              size: 14
            }
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#1db954',
          bodyColor: '#ffffff',
          bodyFont: {
            size: 14
          },
          padding: 12,
          displayColors: false,
          callbacks: {
            title: function(context) {
              return 'User Growth Statistics';
            },
            label: function(context) {
              return `Users: ${context.raw}`;
            }
          }
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeOutQuart'
      },
      layout: {
        padding: {
          top: 20,
          right: 30,
          bottom: 20,
          left: 20
        }
      }
    }
  });

  console.log("Growth chart rendered with data:", data);
};

// Initialize data on component mount
onMounted(() => {
  checkServerStatus();
  fetchUserStats();
  fetchUserGrowth();
  fetchTopGenres();

  // Set up periodic status check (every 30 seconds)
  const statusInterval = setInterval(checkServerStatus, 30000);
  
  // Clean up interval and chart when component is unmounted
  onUnmounted(() => {
    clearInterval(statusInterval);
    if (growthChart.value && growthChart.value.chart) {
      growthChart.value.chart.destroy();
    }
  });
});
</script>

<style scoped>
.admin-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  color: var(--text-color);
}

h1 {
  margin-bottom: 1rem;
  color: var(--primary-color);
  font-size: 2rem;
  text-align: center;
}

/* Admin actions styling */
.admin-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.admin-console-btn, .map-link-btn {
  background-color: var(--secondary-color);
  color: var(--text-color);
  border: 2px solid var(--primary-color);
  border-radius: var(--border-radius);
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
  text-decoration: none;
}

.admin-console-btn:hover, .map-link-btn:hover {
  background-color: var(--primary-color);
  color: var(--secondary-color);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.admin-console-icon, .map-icon {
  font-size: 1.2rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.status-card, .stats-card, .chart-card {
  background-color: var(--glassmorphism-bg);
  backdrop-filter: blur(var(--glassmorphism-blur));
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--box-shadow);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

h2 {
  font-size: 1.3rem;
  margin-bottom: 1.2rem;
  color: var(--primary-color);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.server-status {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  font-size: 1.2rem;
  font-weight: 600;
}

.status-indicator {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.online {
  background-color: var(--primary-color);
  box-shadow: 0 0 10px rgba(29, 185, 84, 0.8);
}

.offline {
  background-color: #ff4d4d;
  box-shadow: 0 0 10px rgba(255, 77, 77, 0.8);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  border-radius: var(--border-radius);
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--accent-color);
}

.stat-percentage {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: var(--primary-color);
  font-weight: 600;
}

.chart-container {
  width: 100%;
  height: 300px;
}

/* Styles pour l'aperçu des genres populaires */
.popular-genres-section {
  margin-top: 2.5rem;
  background-color: var(--glassmorphism-bg);
  backdrop-filter: blur(var(--glassmorphism-blur));
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--box-shadow);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.genre-card {
  border-radius: var(--border-radius);
  padding: 1rem;
  text-align: center;
  background-color: var(--primary-color);
  color: var(--secondary-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: var(--box-shadow);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100px;
}

.genre-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.genre-card h4 {
  margin: 0 0 10px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.genre-card .score {
  font-size: 1.3rem;
  font-weight: 700;
  margin-top: auto;
}

.error {
  color: #ff4d4d;
  padding: 1rem;
  background-color: rgba(255, 77, 77, 0.1);
  border-radius: var(--border-radius);
  border: 1px solid rgba(255, 77, 77, 0.3);
}

@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-card {
    grid-column: 1 / -1;
  }
  
  .admin-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .admin-console-btn, .map-link-btn {
    justify-content: center;
  }
  
  .genres-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }
}
</style>