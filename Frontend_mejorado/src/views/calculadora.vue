<template>
    <div class="calculadora-container">
      <router-link to="/" class="back-button">Regresar a Inicio</router-link>

      <h1>Calculadora de Materiales</h1>

  
      <form @submit.prevent="agregarPrenda">
        <label for="prenda">Selecciona la prenda:</label>
        <select id="prenda" v-model="prenda">
          <option disabled value="">-- Selecciona una prenda --</option>
          <option v-for="(detalle, key) in datos" :key="key" :value="key">
            {{ labels[key] }}
          </option>
        </select>
  
        <label for="talla">Talla:</label>
        <select id="talla" v-model="talla">
          <option disabled value="">-- Selecciona una talla --</option>
          <option value="S">S</option>
          <option value="M">M</option>
          <option value="L">L</option>
          <option value="XL">XL</option>
        </select>
  
        <label for="cantidad">Cantidad de prendas:</label>
        <input
          type="number"
          id="cantidad"
          v-model.number="cantidad"
          min="1"
          required
        />
  
        <button type="submit">Agregar prenda</button>
      </form>
  
      <div v-if="lista.length > 0" class="lista">
        <h2>Prendas seleccionadas</h2>
        <ul>
          <li v-for="(item, index) in lista" :key="index">
            {{ labels[item.prenda] }} - Talla {{ item.talla }} (x{{ item.cantidad }})
          </li>
        </ul>
        <button @click="calcularTotales">Calcular Totales</button>
      </div>
  
      <div v-if="resultado.length > 0" class="resultado">
        <h2>Totales por Categoría</h2>
        <div v-for="(cat, index) in resultado" :key="index" class="bloque-categoria">
          <h3>{{ cat.categoria }}</h3>
          <p><strong>Tela:</strong> {{ cat.tela.toFixed(2) }} m</p>
          <p><strong>Hilo:</strong> {{ cat.hilo.toFixed(2) }} m</p>
          <p><strong>Botones:</strong> {{ cat.botones }}</p>
          <p v-if="cat.elastico > 0"><strong>Elástico:</strong> {{ cat.elastico.toFixed(2) }} m</p>
          <p><strong>Telas Usadas:</strong></p>
          <ul>
            <li v-for="(info, i) in cat.detalles" :key="i">
              {{ info.tipo }} ({{ info.color }}) - {{ info.caracteristicas }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CalculadoraMateriales",
    data() {
      return {
        prenda: "",
        talla: "",
        cantidad: 1,
        lista: [],
        resultado: [],
        multiplicadorPorTalla: {
          S: 1.0,
          M: 1.1,
          L: 1.2,
          XL: 1.3
        },
        datos: {
          pantalon: {
            categoria: "Pantalones",
            tela: 1.8, hilo: 40, botones: 2, elastico: 0.5,
            tipo_tela: "Gabardina", color: "Beige", caracteristicas: "Resistente y formal"
          },
          filipina: {
            categoria: "Prendas Médicas",
            tela: 1.5, hilo: 35, botones: 4, elastico: 0,
            tipo_tela: "Microfibra", color: "Blanca", caracteristicas: "Antifluido, fresca"
          },
          bata: {
            categoria: "Prendas Médicas",
            tela: 2.5, hilo: 50, botones: 4, elastico: 0,
            tipo_tela: "Algodón", color: "Blanca", caracteristicas: "Cómoda y suelta"
          },
          gorro: {
            categoria: "Prendas Médicas",
            tela: 0.5, hilo: 10, botones: 0, elastico: 0.5,
            tipo_tela: "Poliéster", color: "Verde", caracteristicas: "Liviano y lavable"
          },
          camisa_polo: {
            categoria: "Camisas",
            tela: 1.3, hilo: 25, botones: 2, elastico: 0,
            tipo_tela: "Piqué", color: "Azul", caracteristicas: "Casual y flexible"
          },
          camisa_formal: {
            categoria: "Camisas",
            tela: 1.8, hilo: 30, botones: 6, elastico: 0,
            tipo_tela: "Popelina", color: "Celeste", caracteristicas: "Ligera, fácil de planchar"
          },
          camisa_outdoor: {
            categoria: "Camisas",
            tela: 2.0, hilo: 35, botones: 6, elastico: 0,
            tipo_tela: "Ripstop", color: "Gris", caracteristicas: "Resistente al agua"
          },
          pantalon_tela: {
            categoria: "Pantalones",
            tela: 1.8, hilo: 40, botones: 2, elastico: 0.5,
            tipo_tela: "Gabardina", color: "Azul oscuro", caracteristicas: "Formal y duradero"
          },
          gorra: {
            categoria: "Gorras",
            tela: 0.5, hilo: 15, botones: 0, elastico: 0.5,
            tipo_tela: "Lona", color: "Negro", caracteristicas: "Ajustable y resistente"
          }
        },
        labels: {
          pantalon: "Pantalón",
          filipina: "Filipina",
          bata: "Bata",
          gorro: "Gorro quirúrgico",
          camisa_polo: "Camisa Polo",
          camisa_formal: "Camisa Formal",
          camisa_outdoor: "Camisa Outdoor",
          pantalon_tela: "Pantalón de Tela",
          gorra: "Gorra"
        }
      };
    },
    methods: {
      agregarPrenda() {
        if (this.prenda && this.cantidad > 0 && this.talla) {
          this.lista.push({ prenda: this.prenda, cantidad: this.cantidad, talla: this.talla });
          this.prenda = "";
          this.talla = "";
          this.cantidad = 1;
          this.resultado = [];
        }
      },
      calcularTotales() {
        const resumen = {};
        for (const item of this.lista) {
          const datos = this.datos[item.prenda];
          const mult = this.multiplicadorPorTalla[item.talla] || 1;
          const cat = datos.categoria;
  
          if (!resumen[cat]) {
            resumen[cat] = {
              categoria: cat,
              tela: 0,
              hilo: 0,
              botones: 0,
              elastico: 0,
              detalles: new Set()
            };
          }
  
          resumen[cat].tela += datos.tela * mult * item.cantidad;
          resumen[cat].hilo += datos.hilo * mult * item.cantidad;
          resumen[cat].botones += datos.botones * item.cantidad;
          resumen[cat].elastico += datos.elastico * mult * item.cantidad;
          resumen[cat].detalles.add(JSON.stringify({
            tipo: datos.tipo_tela,
            color: datos.color,
            caracteristicas: datos.caracteristicas
          }));
        }
  
        // Convert Set to array de objetos únicos
        this.resultado = Object.values(resumen).map(cat => ({
          ...cat,
          detalles: Array.from(cat.detalles).map(str => JSON.parse(str))
        }));
      }
    }
  };
  </script>
  
  <style scoped>
  .calculadora-container {
    max-width: 650px;
    margin: 40px auto;
    background-color: var(--color-quaternary);
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(55, 70, 102, 0.2);
  }
  
  form {
    display: flex;
    flex-direction: column;
  }
  
  label {
    margin-top: 15px;
    font-weight: bold;
    color: var(--color-senary);
  }
  
  select,
  input {
    padding: 8px;
    border-radius: 5px;
    border: 1px solid var(--color-septenary);
    margin-top: 5px;
  }
  
  button {
    margin-top: 20px;
  }
  
  .lista {
    margin-top: 30px;
    background-color: var(--color-octonary);
    padding: 15px;
    border-radius: 10px;
  }
  
  .resultado {
    margin-top: 30px;
    background-color: var(--color-octonary);
    padding: 20px;
    border-radius: 8px;
    border-left: 6px solid var(--color-primary);
  }
  
  .bloque-categoria {
    margin-bottom: 25px;
  }
  </style>
  