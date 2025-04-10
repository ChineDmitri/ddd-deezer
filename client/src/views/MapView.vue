<template>
  <div class="map-container">
    <div class="age-selector">
      <label for="age-select">Tranche d'âge :</label>
      <select id="age-select" v-model="selectedAge">
        <option value="Jeune">Jeune</option>
        <option value="Adulte">Adulte</option>
        <option value="Senior">Senior</option>
      </select>
    </div>

    <svg class="map-svg" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet">
      <!-- Render each region as a path element -->
      <path v-for="region in regionArray" :key="region.id" :d="region.path" :fill="region.color" class="region"
        stroke="#000000" stroke-width="0.5" @click="handleRegionClick(region)" @mouseover="hoverRegion(region)"
        @mouseout="unhoverRegion(region)" />
    </svg>

    <!-- Afficher le nom de la région sélectionnée -->
    <div v-if="selectedRegionName" class="region-info">
      Région: {{ selectedRegionName }}
    </div>

    <!-- Afficher les résultats des genres musicaux populaires -->
    <div v-if="popularGenres.length > 0" class="genres-container">
      <h3>Genres populaires pour {{ selectedRegionName }} ({{ selectedAge }})</h3>
      <div class="genres-grid">
        <div v-for="(genre, index) in popularGenres" :key="index" class="genre-card">
          <h4>{{ genre.genre }}</h4>
          <div class="score">{{ genre.score }}</div>
        </div>
      </div>
    </div>

    <!-- Afficher le message de chargement -->
    <div v-if="isLoading" class="loading">Chargement des données...</div>

    <!-- Afficher le message d'erreur -->
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<style>
.map-container {
  margin: 0 auto;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: auto;
  position: relative;
}

.map-svg {
  width: 100%;
  height: 70vh;
  max-width: 100%;
  display: block;
}

.region {
  cursor: pointer;
  transition: fill 0.3s ease;
}

.region:hover {
  fill: #FFD700;
}

.region-info {
  position: absolute;
  top: 20px;
  left: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 1.2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.age-selector {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px 20px;
  border-radius: 5px;
  z-index: 10;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.age-selector select {
  padding: 5px 10px;
  border-radius: 4px;
  margin-left: 10px;
}

.genres-container {
  width: 90%;
  max-width: 1000px;
  margin-top: 20px;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.genre-card {
  background-color: #f5f5f5;
  border-radius: 6px;
  padding: 12px;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.genre-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.genre-card h4 {
  margin: 0 0 8px 0;
  font-size: 1rem;
}

.genre-card .score {
  font-weight: bold;
  color: #d35400;
}

.loading,
.error {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(255, 255, 255, 0.9);
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.error {
  color: #e74c3c;
}
</style>

<script lang="js">
import mapData from '@/assets/map.json';
import { getRegionForDepartment, getDepartmentsForRegion, getAllRegions } from '@/services/regionService';
import { getAccessToken } from '@/services/authService';

export default {
  name: 'MapView',
  data() {
    return {
      regions: mapData,
      couleurs: {}, // Stocke les couleurs des régions
      selectedRegionName: null, // Pour stocker le nom de la région sélectionnée
      selectedAge: 'Adulte', // Par défaut, l'âge sélectionné est Adulte
      popularGenres: [], // Pour stocker les genres musicaux populaires
      isLoading: false,
      error: null,
    };
  },
  computed: {
    // Convert the regions object into an array for easier rendering
    regionArray() {
      return Object.keys(this.regions).map((key) => ({
        id: key,
        ...this.regions[key],
        color: this.couleurs[key] || '#CCCCCC', // Couleur par défaut si non définie
      }));
    },
  },
  methods: {
    async handleRegionClick(region) {
      const departmentCode = region.id;
      const regionName = getRegionForDepartment(departmentCode);

      this.selectedRegionName = regionName
        ? regionName
        : `Région inconnue pour le département ${region.name} (${departmentCode})`;

      console.log('Département:', region.name, '(Code:', departmentCode, ') - Région:', this.selectedRegionName);

      // Si une région valide est sélectionnée, récupérer les genres populaires
      if (regionName) {
        await this.fetchPopularGenres(regionName, this.selectedAge);
      }
    },

    async fetchPopularGenres(region, age) {
      this.isLoading = true;
      this.error = null;
      this.popularGenres = [];

      try {
        const url = new URL('http://127.0.0.1:8000/api/music/popular-genres-region-age/');
        url.searchParams.append('region', region);
        url.searchParams.append('age', age);

        // Récupérer le token d'accès
        const accessToken = getAccessToken();

        // Configurer les options de la requête avec le token d'authentification
        const options = {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        };

        // Ajouter le header d'authentification si un token est disponible
        if (accessToken) {
          options.headers['Authorization'] = `Bearer ${accessToken}`;
        }

        const response = await fetch(url, options);

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();
        this.popularGenres = data.genres;
        console.log('Genres populaires récupérés:', this.popularGenres);
      } catch (err) {
        console.error('Erreur lors de la récupération des genres populaires:', err);
        this.error = 'Impossible de récupérer les genres musicaux populaires. Veuillez réessayer.';
      } finally {
        this.isLoading = false;
      }
    },

    hoverRegion(region) {
      console.log('Hovering over:', region.name);
    },

    unhoverRegion(region) {
      console.log('Stopped hovering over:', region.name);
    },

    addRegion(depts, name, color) {
      for (const dept of depts) {
        this.couleurs[dept] = color;
      }
    },
  },
  watch: {
    // Réagir aux changements de la tranche d'âge sélectionnée
    selectedAge(newAge) {
      // Si une région est déjà sélectionnée, mettre à jour les genres populaires
      if (this.selectedRegionName) {
        this.fetchPopularGenres(this.selectedRegionName, newAge);
      }
    }
  },
  mounted() {
    const colors = [
      '#fefaec', // jaune très clair
      '#fcf0c9', // crème doux
      '#f8e08f', // jaune doré
      '#f5ca54', // jaune vif
      '#f2b52d', // or soutenu
      '#eb9515', // orange vif
      '#c76b0e', // orange foncé
      '#8d3d13', // brique
      '#996c57', // brun rosé
      '#bfa28a', // beige chaud
      '#8f5e50', // vieux rose brun
      '#d5c3b2', // sable doux
      '#784b45', // chocolat moyen
      '#ebe2da', // beige rosé très clair
      '#ad4f10', // rouille intense
    ];

    // Iterate through all regions from regionService
    getAllRegions().forEach((regionName, index) => {
      const departments = getDepartmentsForRegion(regionName);
      const colorIndex = index % colors.length;
      this.addRegion(departments, regionName, colors[colorIndex]);
    });
  },
};
</script>