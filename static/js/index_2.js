document.addEventListener('DOMContentLoaded', function() {
  const sliders = document.querySelectorAll('.slider');
  
  sliders.forEach(slider => {
    const container = slider.closest('.images-container');
    const beforeImage = container.querySelector('.before-image');
    const sliderLine = container.querySelector('.slider-line');
    const sliderIcon = container.querySelector('.slider-icon');
    const sliderThumb = container.querySelector('.slider-thumb');
    
    updateSliderPosition(slider.value);
    
    function updateSliderPosition(value) {
      container.style.setProperty('--slider-pos', `${value}%`);
    }
    
    slider.addEventListener('input', function() {
      updateSliderPosition(this.value);
    });
    
    container.addEventListener('click', function(e) {
      if (e.target !== slider) {
        const rect = container.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width * 100;
        slider.value = Math.max(0, Math.min(100, pos));
        updateSliderPosition(slider.value);
      }
    });
    
    container.addEventListener('mousemove', function(e) {
      const rect = container.getBoundingClientRect();
      const pos = (e.clientX - rect.left) / rect.width * 100;
      sliderThumb.style.left = `${pos}%`;
    });
    
    slider.addEventListener('mousedown', function(e) {
      e.stopPropagation();
    });
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const sequenceSlider = document.getElementById('sequence-slider');
  const opacitySlider = document.getElementById('opacity-slider');
  const sliderValue = document.getElementById('slider-value');
  
  // 初始化页面时设置值
  // sliderValue.textContent = sequenceSlider.value;
  // 

  function getOpacityPath(value){
    return `./static/images/opacity_distribution_compressed/opacity_iter_${value}.png`;
  }
  // 更新图片路径的格式函数
  function getImagePath(base, type, value) {
    return `./static/images/${base}/render_${type}/test_1/${type}_${value}.png`;
  }
  
  // FPS图片路径函数
  function getFPSImagePath(value) {
    return `./static/images/bicycle_FPS_compressed/FPS_${value}.png`;
  }

  opacitySlider.addEventListener('input', function() {
    const opacityValue = this.value;
    // Updating Opacity value
    document.getElementById('opacity-image').src = getOpacityPath(opacityValue);
  });

  sequenceSlider.addEventListener('input', function() {
    const frameValue = this.value;
    
    // Updating Baseline 
    document.querySelector('.comparison-col:first-child .after-image').src = 
      getImagePath('render_uv_bicycle_compressed/baseline', 'img', frameValue);
    document.querySelector('.comparison-col:first-child .before-image').src = 
      getImagePath('render_uv_bicycle_compressed/baseline', 'uv', frameValue);
    // Updating + Group Training
    document.querySelector('.comparison-col:nth-child(2) .after-image').src = 
      getImagePath('render_uv_bicycle_compressed/group', 'img', frameValue);
    document.querySelector('.comparison-col:nth-child(2) .before-image').src = 
      getImagePath('render_uv_bicycle_compressed/group', 'uv', frameValue);
    // Updating FPS
    document.getElementById('fps-image').src = getFPSImagePath(frameValue);

  });
});
