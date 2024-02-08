<template>
  <main>
    <div class="file-input-container">
      <label for="file-input" class="glow-on-hover">
        <span>Choisir une image</span>
      </label>
      <input id="file-input" type="file" @change="handleFileChange" class="file-input">
    </div>
    <div class="file-drop-container" ref="dropContainer" @dragover.prevent="handleDragOver" @drop.prevent="handleDrop">
      <p class="drop-text">Glissez-déposez une image ici ou cliquez pour choisir une image</p>
    </div>
    <div class="image-container">
      <img :src="selectedImage" alt="Processed Image" v-if="selectedImage" class="processed-image">
    </div>
    <section class="image-processing-section" v-if="selectedImage">
      <div class="content-container action-buttons">
        <button class="glow-on-hover" @click="processImage('text')">Texte</button>
        <button class="glow-on-hover" @click="processImage('hole')">Texte à trou</button>
      </div>
    </section>
    <section class="loader-container" v-if="loading">
      <div class="loader"></div>
    </section>
    <section v-if="outputText" class="output-container">
      <p class="output-text">{{ outputText }}</p>
    </section>
  </main>
</template>

<script>
export default {
  data() {
    return {
      inputImage: null,
      outputText: null,
      selectedImage: null,
      selectedType: null,
      loading: false
    };
  },
  methods: {
    handleFileChange(event) {
      this.inputImage = event.target.files[0];
      this.selectedImage = URL.createObjectURL(this.inputImage);
      this.outputText = null;
    },
    processImage(type) {
      this.loading = true;
      this.selectedType = type;
      const formData = new FormData();
      formData.append('file', this.inputImage);
      formData.append('type', this.selectedType);

      fetch('http://localhost:5000/process_image', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          console.error('Error processing image:', data.error);
        } else {
          this.outputText = data.processed_text;
        }
      })
      .catch(error => {
        console.error('Error processing image:', error);
      })
      .finally(() => {
        this.loading = false;
      });
    },
    handleDragOver(event) {
      event.preventDefault();
      event.dataTransfer.dropEffect = 'copy';
      // Ajoutez une classe active pour styliser la zone de dépôt
      this.$refs.dropContainer.classList.add('active');
    },
    handleDrop(event) {
      event.preventDefault();
      this.$refs.dropContainer.classList.remove('active');
      const files = event.dataTransfer.files;
      if (files.length > 0) {
        this.handleFileChange({ target: { files: [files[0]] } });
      }
    },
  },
};
</script>

<style scoped>
  main {
    align-items: center;
  }
  .file-input-container {
    text-align: center;
    margin: 20px;
  }
  .image-processing-section {
    text-align: center;
    align-items: center;
    max-width: 500px;
    margin: 20px auto;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
  }

  .file-input {
    opacity: 0;
    position: absolute;
    z-index: -1;
  }

  .content-container {
    max-width:800px;
    flex-direction: column;
  }

  .action-buttons {
    margin-top: 15px;
    margin-bottom: 15px;
    align-items: baseline;
    justify-content: center;
  }

  .loader-container {
    margin: 20px;
  }

  .image-container {
    text-align: center;
    align-items: center;
    max-width: 100%;
    overflow: hidden;
  }

  .processed-image {
    max-width: 98%;
    height: auto;
    border: 4px solid #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    object-fit: contain;
  }

  .output-container {
    margin: 30px;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    text-align: center;
  }

  .output-text {
    font-family: 'Oswald', sans-serif;  
    animation-duration: 3s;
    animation-name: slidein;
    font-size: 18px;
    color: #333;
  }
  @keyframes slidein {
    from {
      margin-left: 100%;
      width: 300%;
    }
    to {
      margin-left: 0%;
      width: 100%;
    }
  }

  .loader {
    border: 8px solid #ffffff;
    border-top: 8px solid #000000;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
    margin-top: 20px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .glow-on-hover {
    font-family: 'Oswald', sans-serif;
    background: none;
    border: 2px solid;
    font: inherit;
    line-height: 1;
    margin: 0.5em;
    padding: 1em 2em;
    width: 220px;
    height: 50px;
    border: none;
    outline: none;
    color: #fff;
    background: #111;
    cursor: pointer;
    position: relative;
    z-index: 0;
    border-radius: 10px;
  }

  .glow-on-hover:before {
      content: '';
      background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
      position: absolute;
      top: -2px;
      left:-2px;
      background-size: 400%;
      z-index: -1;
      filter: blur(5px);
      width: calc(100% + 4px);
      height: calc(100% + 4px);
      animation: glowing 20s linear infinite;
      opacity: 0;
      transition: opacity .3s ease-in-out;
      border-radius: 10px;
  }

  .glow-on-hover:active {
      color: #000
  }

  .glow-on-hover:active:after {
      background: transparent;
  }

  .glow-on-hover:hover:before {
      opacity: 1;
  }

  .glow-on-hover:after {
      z-index: -1;
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      background: #111;
      left: 0;
      top: 0;
      border-radius: 10px;
  }

  @keyframes glowing {
      0% { background-position: 0 0; }
      50% { background-position: 400% 0; }
      100% { background-position: 0 0; }
  }

  .button-1 {
    width: 200px;
    padding-top: 30px;
    padding-bottom: 30px;
    text-align: center;
    color: #000;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 10px;
    cursor: pointer;
    display: inline-block;
    background-color: transparent;
    border: 1px solid #000000;
    border-radius: 20px;
    transition: all .25s ease-in-out;
  }

  .button-1:hover {
    background-color:#000000;
    border: 1px solid #ffffff;
    color: white;
    box-shadow: 0 0 10px 0 #000000 inset, 0 0 20px 2px #000000;
  }
  .file-drop-container {
    border: 2px dashed #ccc;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    margin: 20px;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }

  .drop-text {
    font-size: 16px;
    color: #555;
  }

  .file-drop-container.active {
    border-color: #007bff;
  }
</style>
