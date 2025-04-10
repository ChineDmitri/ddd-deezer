<template>
  <div class="map-container">
    <svg class="map-svg" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet">
      <!-- Render each region as a path element -->
      <path v-for="region in regionArray" :key="region.id" :d="region.path" :fill="region.color" class="region"
        stroke="#000000" stroke-width="0.5" @click="handleRegionClick(region)" @mouseover="hoverRegion(region)"
        @mouseout="unhoverRegion(region)" />
    </svg>
  </div>
</template>

<style>
.map-container {
  margin: 0 auto;
  width: 100%;
  height: 100vh;
  /* Utilise toute la hauteur de la fenêtre */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  /* Empêche les débordements */
}

.map-svg {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  display: block;
}

.region {
  cursor: pointer;
  transition: fill 0.3s ease;
  /* Animation pour le changement de couleur */
}

.region:hover {
  fill: #FFD700;
  /* Couleur dorée au survol */
}
</style>

<script lang="js">
import mapData from '@/assets/map.json';

export default {
  name: 'MapView',
  data() {
    return {
      regions: mapData,
      couleurs: {}, // Stocke les couleurs des régions
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
    handleRegionClick(region) {
      console.log('Region clicked:', region.name);
      // Ajoutez ici une logique supplémentaire si nécessaire
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
  mounted() {
    // Ajoutez les régions et leurs couleurs
    this.addRegion(['62', '59'], 'Nord pas-de-calais', '#FF5733');
    this.addRegion(['80', '02', '60'], 'Picardie', '#33FF57');
    this.addRegion(['76', '27'], 'Haute normandie', '#3357FF');
    this.addRegion(['08', '51', '52', '10'], 'Champagne Ardennes', '#FF33A1');
    this.addRegion(['57', '88', '54', '55'], 'Lorraine', '#FF5733');
    this.addRegion(['67', '68'], 'Alsace', '#3357FF');
    this.addRegion(['50', '61', '14'], 'Basse Normandie', '#FF33A1');
    this.addRegion(['75', '77', '91', '95', '78', '93', '94', '92'], 'Ile de France', '#FF5733');
    this.addRegion(['22', '35', '29', '56'], 'Bretagne', '#3357FF');
    this.addRegion(['49', '53', '72', '85', '44'], 'Pays de loire', '#FF5733');
    this.addRegion(['45', '18', '41', '36', '37', '28'], 'Centre', '#33FF57');
    this.addRegion(['71', '21', '58', '89'], 'Bourgogne', '#3357FF');
    this.addRegion(['39', '25', '70', '90'], 'Franche compté', '#33FF57');
    this.addRegion(['17', '79', '16', '86'], 'Poitou charente', '#FF33A1');
    this.addRegion(['87', '23', '19'], 'Limousin', '#FF5733');
    this.addRegion(['63', '43', '03', '15'], 'Auvergne', '#FF33A1');
    this.addRegion(['07', '01', '26', '38', '73', '74', '42', '69'], 'Rhone-alpes', '#FF5733');
    this.addRegion(['33', '47', '24', '64', '40'], 'Aquitaine', '#3357FF');
    this.addRegion(['46', '12', '81', '32', '82', '65', '09', '31'], 'Midi pyrénées', '#33FF57');
    this.addRegion(['66', '48', '11', '34', '30'], 'Languedoc roussillon', '#3357FF');
    this.addRegion(['13', '83', '84', '04', '05', '06'], 'Paca', '#FF33A1');
    this.addRegion(['2B', '2A'], 'Corse', '#FF5733');
    this.addRegion(['971', '972', '973', '974'], 'DOM', '#33FF57');
  },
};
</script>