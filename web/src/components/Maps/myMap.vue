<template>
  <div>
    <l-map :zoom="zoom" :center="center" style="height: 500px; width: 100%">
      <l-tile-layer :url="url" :attribution="attribution" />
      <l-marker
        :key="index"
        v-for="(centro, index) in centros"
        :lat-lng="latLng(centro.latitud, centro.longitud)"
      >
        <l-popup>
          Nombre: {{ centro.nombre }}<br />
          Telefono: {{ centro.telefono }}<br />
          Direccion: {{ centro.direccion }}<br />
          Horarios: {{ centro.hora_inicio }}-{{ centro.hora_fin }}
          <b-form @submit.stop.prevent="onSubmit(centro.id)">
            <b-form-group>
              <b-form-input
                v-model.number="centro.id"
                type="text"
                required
                value="centro.id"
                hidden
              ></b-form-input>
            </b-form-group>

            <b-form-group>
              <b-calendar v-model="fecha" :min="today_min"></b-calendar>
            </b-form-group>

            <b-button type="submit" variant="primary" :disabled="!fecha"
              >Reservar Turno</b-button
            >
          </b-form>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<script>
import axios from 'axios';
import L from 'leaflet';
import { LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';

export default {
  name: 'myMap',
  props: {
    centros: Array,
  },
  data() {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    return {
      today_min: today,
      zoom: 6,
      center: [-36.5635, -60.1076],
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      marker: L.latLng(-34.9159, -57.9924),
      fecha: '',
    };
  },
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  methods: {
    onSubmit(centro_id) {
      this.$router.push({
        name: 'turno',
        params: { id: centro_id, fecha: this.fecha },
      });
    },
    latLng: function(lat, lng) {
      return L.latLng(lat, lng);
    },
  },

  mounted: function() {
    axios
      .get('https://admin-grupo37.proyecto2020.linti.unlp.edu.ar/api/centros')
      .then((result) => {
        this.centros = result.data.centros;
      });
  },
};
</script>
