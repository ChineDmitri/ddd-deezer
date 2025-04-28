<template>
  <div class="map-container">
    <!-- La carte est maintenant en premier -->
    <div class="map-wrapper">
      <svg class="map-svg" viewBox="0 0 750 750" preserveAspectRatio="xMidYMid meet">
        <path v-for="region in regionArray" :key="region.id" :d="region.path" :fill="region.color" class="region"
          stroke="#503a33" stroke-width="0.5" @click="handleRegionClick(region)" @mouseover="hoverRegion(region)"
          @mouseout="unhoverRegion(region)" />
      </svg>
    </div>

    <!-- Controls déplacés sous la carte -->
    <div class="control-section">
      <div class="header-controls">
        <div v-if="selectedRegionName" class="region-info">
          <span class="region-label">Région:</span>
          <span class="region-name">{{ selectedRegionName }}</span>
        </div>

        <div class="age-selector">
          <label for="age-select">Tranche d'âge:</label>
          <select id="age-select" v-model="selectedAge">
            <option value="Jeune">Jeune</option>
            <option value="Adulte">Adulte</option>
            <option value="Senior">Senior</option>
          </select>
        </div>
      </div>

      <!-- Pour les artistes: afficher le graphique global pour la région -->
      <div v-if="isArtist && selectedRegionName && showRegionChart" class="chart-container">
        <div class="chart-controls">
          <h3 class="chart-title">Popularité des genres - {{ selectedRegionName }}</h3>
          <button class="chart-toggle-button" @click="toggleView">
            Voir par tranche d'âge
          </button>
        </div>
        <div class="chart-wrapper">
          <canvas ref="pieChart"></canvas>
        </div>
      </div>

      <!-- Afficher les résultats des genres musicaux populaires par âge -->
      <div v-if="popularGenres.length > 0 && (!isArtist || !showRegionChart)" class="genres-container">
        <div v-if="isArtist" class="chart-controls">
          <h3 class="genres-title">Genres musicaux populaires</h3>
          <button class="chart-toggle-button" @click="toggleView">
            Voir vue globale
          </button>
        </div>
        <div v-else class="genres-title-container">
          <h3 class="genres-title">Genres musicaux populaires</h3>
        </div>
        <div class="genres-subtitle">{{ selectedRegionName }} - {{ selectedAge }}</div>
        <div class="genres-grid">
          <div v-for="(genre, index) in popularGenres" :key="index" class="genre-card"
            @click="showGenreMetrics(genre.genre)">
            <h4>{{ genre.genre }}</h4>
            <div class="score">{{ genre.score }}</div>
          </div>
        </div>
      </div>

      <!-- Modal pour afficher les métriques d'un genre -->
      <div v-if="showMetricsModal" class="metrics-modal-overlay" @click.self="closeModal">
        <div class="metrics-modal">
          <div class="metrics-modal-header">
            <h3>Métriques pour le genre <span class="genre-name">{{ selectedGenre }}</span></h3>
            <button class="close-modal-button" @click="closeModal">×</button>
          </div>
          <div v-if="loadingMetrics" class="metrics-loading">
            <div class="spinner"></div> Chargement des métriques...
          </div>
          <div v-else-if="metricsError" class="metrics-error">
            {{ metricsError }}
          </div>
          <div v-else-if="genreMetrics" class="metrics-content">
            <div class="metrics-grid">
              <div class="metric-item">
                <div class="metric-label">BPM</div>
                <div class="metric-value">{{ genreMetrics.metrics.bpm }}</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Gain</div>
                <div class="metric-value">{{ genreMetrics.metrics.gain }} dB</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Durée moyenne</div>
                <div class="metric-value">{{ genreMetrics.metrics.duration_minutes.toFixed(2) }} min</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Dansabilité</div>
                <div class="metric-value">{{ (genreMetrics.metrics.danceability * 100).toFixed(0) }}%</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Énergie</div>
                <div class="metric-value">{{ (genreMetrics.metrics.energy * 100).toFixed(0) }}%</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Acoustique</div>
                <div class="metric-value">{{ (genreMetrics.metrics.acousticness * 100).toFixed(0) }}%</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Instrumental</div>
                <div class="metric-value">{{ (genreMetrics.metrics.instrumentalness * 100).toFixed(0) }}%</div>
              </div>
              <div class="metric-item">
                <div class="metric-label">Valence</div>
                <div class="metric-value">{{ (genreMetrics.metrics.valence * 100).toFixed(0) }}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages d'état -->
    <div v-if="isLoading" class="status-message loading">
      <div class="spinner"></div> Chargement des données...
    </div>

    <div v-if="error" class="status-message error">
      <span class="error-icon">!</span> {{ error }}
    </div>
  </div>
</template>

<style>
:root {
  --muesli-50: #f6f5f0;
  --muesli-100: #eae3d7;
  --muesli-200: #d6c9b2;
  --muesli-300: #bea886;
  --muesli-400: #a98960;
  --muesli-500: #9c7a56;
  --muesli-600: #866348;
  --muesli-700: #6c4d3c;
  --muesli-800: #5c4237;
  --muesli-900: #503a33;
  --muesli-950: #2d1f1b;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--muesli-50);
  margin: 0;
  padding: 0;
}

.map-container {
  margin: 0 auto;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
}

.map-wrapper {
  width: 100%;
  height: 70vh;
  /* Plus grande pour mettre l'accent sur la carte */
  position: relative;
  margin-bottom: 20px;
}

.map-svg {
  width: 100%;
  height: 100%;
  max-width: 100%;
  display: block;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.control-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header-controls {
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 10px 15px;
  box-sizing: border-box;
  z-index: 10;
  margin-bottom: 15px;
}

.region {
  cursor: pointer;
  transition: fill 0.3s ease, stroke-width 0.3s ease;
}

.region:hover {
  fill: var(--muesli-200) !important;
  stroke-width: 1.5;
}

.region-info {
  background-color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 1.1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-left: 5px solid var(--muesli-500);
}

.region-label {
  color: var(--muesli-700);
  font-weight: 500;
}

.region-name {
  font-weight: 600;
  color: var(--muesli-800);
}

.age-selector {
  background-color: white;
  padding: 10px 20px;
  border-radius: 8px;
  z-index: 10;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  border-right: 5px solid var(--muesli-500);
}

.age-selector label {
  color: var(--muesli-700);
  font-weight: 500;
  margin-right: 10px;
}

.age-selector select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid var(--muesli-300);
  background-color: white;
  color: var(--muesli-800);
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
}

.age-selector select:hover,
.age-selector select:focus {
  border-color: var(--muesli-500);
  box-shadow: 0 0 0 2px rgba(156, 122, 86, 0.2);
}

.genres-container {
  width: 90%;
  max-width: 1200px;
  margin-top: 20px;
  margin-bottom: 40px;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.genres-title {
  font-size: 1.5rem;
  color: var(--muesli-800);
  margin: 0 0 5px 0;
  font-weight: 600;
  text-align: center;
}

.genres-title-container {
  text-align: center;
  margin-bottom: 5px;
}

.genres-subtitle {
  color: var(--muesli-600);
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--muesli-100);
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.genre-card {
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: var(--muesli-500);
  color: white;
  min-height: 80px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.genre-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.genre-card::after {
  /* N'afficher l'icône que pour certains rôles - on supprime l'attribut content ici */
  position: absolute;
  bottom: 5px;
  right: 5px;
  font-size: 12px;
  opacity: 0.7;
  transition: opacity 0.2s ease;
}

/* Ajouter cette classe pour les utilisateurs admin et artist */
.artist-view .genre-card::after,
.admin-view .genre-card::after {
  content: "📊";
  /* Icône de statistiques pour admin/artist */
}

/* La classe hover reste pour tous */
.genre-card:hover::after {
  opacity: 1;
}

.genre-card h4 {
  margin: 0 0 10px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.genre-card .score {
  font-size: 1.2rem;
  font-weight: 700;
  padding: 3px 0;
}

.chart-container {
  width: 90%;
  max-width: 1200px;
  margin-top: 20px;
  margin-bottom: 40px;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.chart-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-title {
  font-size: 1.5rem;
  color: var(--muesli-800);
  margin: 0;
  font-weight: 600;
}

.chart-toggle-button {
  padding: 8px 16px;
  background-color: var(--muesli-500);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.chart-toggle-button:hover {
  background-color: var(--muesli-600);
}

.chart-wrapper {
  height: 350px;
  position: relative;
}

.metrics-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.metrics-modal {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.metrics-modal-header {
  background-color: var(--muesli-500);
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metrics-modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.genre-name {
  font-weight: 700;
}

.close-modal-button {
  background: none;
  border: none;
  color: white;
  font-size: 1.8rem;
  cursor: pointer;
  line-height: 1;
}

.metrics-content {
  padding: 20px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.metric-item {
  background-color: var(--muesli-50);
  border-radius: 8px;
  padding: 15px;
  border-left: 4px solid var(--muesli-300);
}

.metric-label {
  font-size: 0.9rem;
  color: var(--muesli-700);
  margin-bottom: 5px;
}

.metric-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--muesli-900);
}

.metrics-loading {
  padding: 30px;
  text-align: center;
  color: var(--muesli-700);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.metrics-error {
  padding: 20px;
  color: #e74c3c;
  text-align: center;
  font-weight: 500;
}

.status-message {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  padding: 10px 20px;
  border-radius: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  font-weight: 500;
  z-index: 100;
}

.loading {
  color: var(--muesli-700);
}

.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid rgba(156, 122, 86, 0.2);
  border-top: 3px solid var(--muesli-500);
  border-radius: 50%;
  margin-right: 8px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.error {
  color: #e74c3c;
  background-color: #fdf3f2;
  border-left: 4px solid #e74c3c;
}

.error-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background-color: #e74c3c;
  color: white;
  font-weight: bold;
  margin-right: 8px;
}
</style>

<script lang="js">
import mapData from '@/assets/map.json';
import { getRegionForDepartment, getDepartmentsForRegion, getAllRegions } from '@/services/regionService';
import { getAccessToken, getRoleBasedApiUrl, getCurrentUserRole } from '@/services/authService';
import { Chart } from 'chart.js/auto';

// API base URL constant
const API_BASE_URL = 'http://127.0.0.1:8000/api';

export default {
  name: 'MapView',
  data() {
    return {
      regions: mapData,
      couleurs: {},
      selectedRegionName: null,
      selectedAge: 'Adulte',
      popularGenres: [],
      isLoading: false,
      error: null,
      chart: null,
      showRegionChart: true, // Par défaut, afficher la vue globale pour les artistes
      regionGenresData: null, // Pour stocker les données globales de la région
      showMetricsModal: false,
      selectedGenre: null,
      genreMetrics: null,
      loadingMetrics: false,
      metricsError: null,
    };
  },
  computed: {
    regionArray() {
      return Object.keys(this.regions).map((key) => ({
        id: key,
        ...this.regions[key],
        color: this.couleurs[key] || '#d6d6d6',
      }));
    },
    isArtist() {
      // Permettre aux admins de voir les mêmes fonctionnalités que les artistes
      const role = getCurrentUserRole();
      return role === 'artist' || role === 'admin';
    },
  },
  methods: {
    async handleRegionClick(region) {
      const departmentCode = region.id;
      const regionName = getRegionForDepartment(departmentCode);

      this.selectedRegionName = regionName
        ? regionName
        : `Région inconnue pour le département ${region.name} (${departmentCode})`;

      // Si une région valide est sélectionnée
      if (regionName) {
        if (this.isArtist) {
          // Pour les artistes et admins, récupérer à la fois les données globales et par âge
          await Promise.all([
            this.fetchArtistRegionGenres(regionName),
            this.fetchPopularGenres(regionName, this.selectedAge)
          ]);
        } else {
          // Pour les auditeurs, récupérer uniquement les données par âge
          await this.fetchPopularGenres(regionName, this.selectedAge);
        }
      }
    },

    async fetchPopularGenres(region, age) {
      this.isLoading = true;
      this.error = null;

      try {
        // URL spécifique selon le rôle de l'utilisateur
        let apiUrl;
        const userRole = getCurrentUserRole();

        if (userRole === 'artist') {
          apiUrl = `${API_BASE_URL}/music/artists/popular-genres-region-age/`;
        } else if (userRole === 'admin') {
          // Les administrateurs utilisent le même endpoint que les artistes
          apiUrl = `${API_BASE_URL}/music/artists/popular-genres-region-age/`;
        } else {
          apiUrl = getRoleBasedApiUrl('popular-genres-region-age');
        }

        const url = new URL(apiUrl);
        url.searchParams.append('region', region);
        url.searchParams.append('age', age);

        const accessToken = getAccessToken();
        const options = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        };

        if (accessToken) {
          options.headers['Authorization'] = `Bearer ${accessToken}`;
        }

        const response = await fetch(url, options);

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();
        this.popularGenres = data.genres;
      } catch (err) {
        console.error('Erreur lors de la récupération des genres populaires:', err);
        this.error = 'Impossible de récupérer les genres musicaux populaires. Veuillez réessayer.';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchArtistRegionGenres(region) {
      try {
        const apiUrl = `${API_BASE_URL}/music/artists/popular-genres-region/`;
        const url = new URL(apiUrl);
        url.searchParams.append('region', region);

        const accessToken = getAccessToken();
        const options = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        };

        if (accessToken) {
          options.headers['Authorization'] = `Bearer ${accessToken}`;
        }

        const response = await fetch(url, options);

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();
        this.regionGenresData = data;

        if (this.showRegionChart) {
          this.renderPieChart(data.genres);
        }
      } catch (err) {
        console.error('Erreur lors de la récupération des statistiques globales de genres:', err);
        // Ne pas afficher d'erreur ici car c'est une fonctionnalité supplémentaire
      }
    },

    renderPieChart(genres) {
      // Détruire le graphique existant s'il y en a un
      if (this.chart) {
        this.chart.destroy();
      }

      // Organiser les genres par score décroissant pour une meilleure lisibilité
      const sortedGenres = [...genres].sort((a, b) => b.raw_score - a.raw_score);

      // Limiter le nombre de genres affichés pour éviter la surcharge (facultatif)
      const topGenres = sortedGenres.slice(0, 10);

      // Palette de couleurs dans le thème muesli
      const colorPalette = [
        '#9c7a56', // muesli-500
        '#6c4d3c', // muesli-700
        '#d6c9b2', // muesli-200
        '#503a33', // muesli-900
        '#bea886', // muesli-300
        '#2d1f1b', // muesli-950
        '#a98960', // muesli-400
        '#5c4237', // muesli-800
        '#eae3d7', // muesli-100
        '#866348', // muesli-600
      ];

      // Créer un nouveau graphique avec des barres horizontales
      const chartData = {
        labels: topGenres.map(g => g.genre),
        datasets: [{
          label: 'Score de popularité',
          backgroundColor: topGenres.map((_, index) => colorPalette[index % colorPalette.length]),
          data: topGenres.map(g => g.raw_score),
          borderColor: '#FFFFFF',
          borderWidth: 1,
          borderRadius: 6,
          barThickness: 18,
          maxBarThickness: 25
        }]
      };

      // S'assurer que l'élément canvas est disponible
      this.$nextTick(() => {
        if (this.$refs.pieChart) {
          const ctx = this.$refs.pieChart.getContext('2d');
          this.chart = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
              indexAxis: 'y', // Pour un graphique à barres horizontal
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false, // Cacher la légende car les labels sont déjà sur l'axe Y
                },
                tooltip: {
                  callbacks: {
                    label: function (context) {
                      const genre = context.label || '';
                      const score = topGenres[context.dataIndex].score;
                      const rawScore = topGenres[context.dataIndex].raw_score.toFixed(2);
                      return [`Genre: ${genre}`, `Score: ${score}`, `Valeur: ${rawScore}`];
                    },
                    title: function (context) {
                      return 'Statistiques de popularité';
                    }
                  },
                  backgroundColor: 'rgba(79, 58, 51, 0.9)',
                  titleFont: {
                    weight: 'bold',
                    size: 16
                  },
                  bodyFont: {
                    size: 14
                  },
                  padding: 15,
                  displayColors: true
                }
              },
              layout: {
                padding: {
                  top: 20,
                  right: 30,
                  bottom: 20,
                  left: 20
                }
              },
              scales: {
                x: {
                  beginAtZero: true,
                  grid: {
                    color: 'rgba(200, 200, 200, 0.2)',
                  },
                  ticks: {
                    font: {
                      weight: 'bold'
                    }
                  },
                  title: {
                    display: true,
                    text: 'Score brut',
                    font: {
                      weight: 'bold',
                      size: 14
                    }
                  }
                },
                y: {
                  grid: {
                    display: false
                  },
                  ticks: {
                    font: {
                      weight: 'bold',
                      size: 13
                    },
                    padding: 10 // Plus d'espace entre l'étiquette et la barre
                  }
                }
              },
              animation: {
                duration: 1000,
                easing: 'easeOutQuart'
              },
              // Ces deux propriétés contrôlent l'espacement des barres
              barPercentage: 0.7, // Réduit pour espacer davantage (valeur par défaut: 0.9)
              categoryPercentage: 0.8 // Réduit pour espacer davantage (valeur par défaut: 0.8)
            }
          });
        }
      });
    },

    async showGenreMetrics(genre) {
      // Seuls les utilisateurs admin et artist peuvent voir les métriques détaillées
      const userRole = getCurrentUserRole();
      if (userRole !== 'admin' && userRole !== 'artist') {
        return;
      }

      this.selectedGenre = genre;
      this.showMetricsModal = true;
      this.loadingMetrics = true;
      this.metricsError = null;
      this.genreMetrics = null;

      try {
        const apiUrl = `${API_BASE_URL}/music/artists/metrics-genre/`;
        const url = new URL(apiUrl);
        url.searchParams.append('region', this.selectedRegionName);
        url.searchParams.append('genre', genre);

        const accessToken = getAccessToken();
        const options = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        };

        if (accessToken) {
          options.headers['Authorization'] = `Bearer ${accessToken}`;
        }

        const response = await fetch(url, options);

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();
        this.genreMetrics = data;
      } catch (err) {
        console.error('Erreur lors de la récupération des métriques du genre:', err);
        this.metricsError = 'Impossible de récupérer les métriques pour ce genre musical.';
      } finally {
        this.loadingMetrics = false;
      }
    },

    closeModal() {
      this.showMetricsModal = false;
    },

    toggleView() {
      this.showRegionChart = !this.showRegionChart;

      if (this.showRegionChart && this.regionGenresData) {
        this.$nextTick(() => {
          this.renderPieChart(this.regionGenresData.genres);
        });
      }
    },

    hoverRegion(region) {
      // Effet de survol simplifié
    },

    unhoverRegion(region) {
      // Retour à l'état normal
    },

    addRegion(depts, name, color) {
      for (const dept of depts) {
        this.couleurs[dept] = color;
      }
    },
  },
  watch: {
    selectedAge(newAge) {
      if (this.selectedRegionName) {
        this.fetchPopularGenres(this.selectedRegionName, newAge);
      }
    }
  },
  mounted() {
    const colors = [
      '#a98960', // muesli-400
      '#eae3d7', // muesli-100
      '#d6c9b2', // muesli-200
      '#9c7a56', // muesli-500 
      '#bea886', // muesli-300
      '#8b6a4f', // muesli-600 - un peu plus profond
      '#cbb9a0', // muesli-250 - intermédiaire doux
      '#f5f0e8', // muesli-050 - très clair pour contraste
      '#b79c7e', // muesli-350 - ton sable chaud
      '#7a5a41', // muesli-700 - plus rustique, pour contraste
      '#e0d4c2', // muesli-150 - très doux, presque pastel
      '#ad9576', // muesli-375 - un ton noisette doux
      '#dbcab7', // muesli-175 - ton biscuit très clair
      '#6b4c37', // muesli-800 - accent plus marqué
      '#c3ab91', // muesli-275 - entre moyen et clair
    ];

    // Utiliser les couleurs muesli pour colorer la carte
    getAllRegions().forEach((regionName, index) => {
      const departments = getDepartmentsForRegion(regionName);
      const colorIndex = index % colors.length;
      this.addRegion(departments, regionName, colors[colorIndex]);
    });
  },
  beforeDestroy() {
    // Nettoyer le graphique lors de la destruction du composant
    if (this.chart) {
      this.chart.destroy();
    }
  },
};
</script>