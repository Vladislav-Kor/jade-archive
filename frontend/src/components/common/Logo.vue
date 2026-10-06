<template>
  <div class="logo" :class="[size, { animated: animated }]">
    <div class="logo-mark">
      <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="serverGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#00ffcc"/>
            <stop offset="50%" stop-color="#00c49a"/>
            <stop offset="100%" stop-color="#008b6e"/>
          </linearGradient>
          <linearGradient id="cloudGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="rgba(0, 196, 154, 0.3)"/>
            <stop offset="100%" stop-color="rgba(0, 196, 154, 0.02)"/>
          </linearGradient>
        </defs>

        <!-- Облако (основа) -->
        <path d="M12 60 C8 50 16 44 26 46 C30 36 42 34 50 38 C56 32 70 34 74 44 C84 44 88 54 82 62 Z" 
              fill="url(#cloudGrad)" stroke="#00c49a" stroke-width="1.2"/>
        
        <!-- Корпус корабля = СЕРВЕРНАЯ СТОЙКА -->
        <rect x="35" y="48" width="30" height="22" rx="3" stroke="url(#serverGrad)" stroke-width="1.8" fill="none"/>
        
        <!-- Внутренние полки сервера -->
        <line x1="38" y1="54" x2="62" y2="54" stroke="#00c49a" stroke-width="1" opacity="0.6"/>
        <line x1="38" y1="60" x2="62" y2="60" stroke="#00c49a" stroke-width="1" opacity="0.6"/>
        
        <!-- Серверные диски (HDD) на полках -->
        <rect x="40" y="51" width="8" height="3" rx="0.5" fill="#00c49a" opacity="0.7"/>
        <rect x="52" y="51" width="8" height="3" rx="0.5" fill="#00c49a" opacity="0.7"/>
        
        <rect x="40" y="57" width="8" height="3" rx="0.5" fill="#00c49a" opacity="0.5"/>
        <rect x="52" y="57" width="8" height="3" rx="0.5" fill="#00c49a" opacity="0.5"/>

        <!-- Индикаторы активности сервера -->
        <circle cx="40" cy="53" r="1" fill="#ffd54f"/>
        <circle cx="40" cy="59" r="1" fill="#ffd54f"/>
        <circle cx="40" cy="65" r="1" fill="#ffd54f"/>

        <!-- Вентиляторы охлаждения -->
        <circle cx="56" cy="53" r="2.5" stroke="#00c49a" stroke-width="0.6" fill="none"/>
        <circle cx="56" cy="59" r="2.5" stroke="#00c49a" stroke-width="0.6" fill="none"/>
        <circle cx="50" cy="65" r="2.5" stroke="#00c49a" stroke-width="0.6" fill="none"/>

        <!-- Мачта-антенна -->
        <line x1="50" y1="48" x2="50" y2="32" stroke="#00c49a" stroke-width="1.5" stroke-linecap="round"/>
        
        <!-- Парус = СЕТЬ/ПЕРЕДАЧА ДАННЫХ -->
        <path d="M50 35 L65 44 L50 46 Z" fill="url(#serverGrad)" opacity="0.5"/>
        <path d="M50 35 L35 44 L50 46 Z" fill="url(#serverGrad)" opacity="0.3"/>

        <!-- Сигнал Wi-Fi на мачте -->
        <path d="M46 28 C48 25 52 25 54 28" stroke="#ffd54f" stroke-width="1" fill="none" stroke-linecap="round"/>
        <path d="M44 32 C48 27 52 27 56 32" stroke="#ffd54f" stroke-width="0.8" fill="none" stroke-linecap="round" opacity="0.6"/>
        <path d="M42 36 C48 29 52 29 58 36" stroke="#ffd54f" stroke-width="0.6" fill="none" stroke-linecap="round" opacity="0.4"/>

        <!-- Флаг с буквой A -->
        <path d="M50 32 L56 34 L50 36 Z" fill="#ffd54f"/>

        <!-- Нос корабля (передняя часть) -->
        <path d="M35 48 L28 55 L35 62" stroke="#00c49a" stroke-width="1.5" fill="none" stroke-linejoin="round"/>

        <!-- Волны = ПОТОК ДАННЫХ -->
        <path d="M22 68 C30 64 38 72 46 68 C54 64 62 72 70 68 C78 64 86 70 86 70" 
              stroke="#00c49a" stroke-width="1" fill="none" opacity="0.5"/>
        
        <!-- Капли данных (пакеты) -->
        <circle cx="30" cy="66" r="1" fill="#ffd54f" opacity="0.6"/>
        <circle cx="54" cy="66" r="1" fill="#ffd54f" opacity="0.6"/>
        <circle cx="74" cy="66" r="1" fill="#ffd54f" opacity="0.6"/>
      </svg>
    </div>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg', 'xl'].includes(v)
  },
  animated: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.logo-mark {
  flex-shrink: 0;
}

.logo.sm .logo-mark { width: 32px; height: 32px; }
.logo.md .logo-mark { width: 40px; height: 40px; }
.logo.lg .logo-mark { width: 48px; height: 48px; }
.logo.xl .logo-mark { width: 64px; height: 64px; }

/* Анимация облака */
.logo.animated .logo-mark path:first-child {
  animation: cloudFloat 4s ease-in-out infinite;
}

@keyframes cloudFloat {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(2px); }
}

/* Анимация индикаторов сервера */
.logo.animated .logo-mark circle:nth-child(4) { animation: blink 1s infinite; animation-delay: 0s; }
.logo.animated .logo-mark circle:nth-child(5) { animation: blink 1s infinite; animation-delay: 0.3s; }
.logo.animated .logo-mark circle:nth-child(6) { animation: blink 1s infinite; animation-delay: 0.6s; }

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.2; }
}

/* Анимация вентиляторов */
.logo.animated .logo-mark circle:nth-child(7) { animation: spin 2s linear infinite; }
.logo.animated .logo-mark circle:nth-child(8) { animation: spin 2s linear infinite; }
.logo.animated .logo-mark circle:nth-child(9) { animation: spin 2s linear infinite; }

@keyframes spin {
  from { stroke-dasharray: 2 14; transform: rotate(0deg); }
  to { stroke-dasharray: 2 14; transform: rotate(360deg); }
}

/* Анимация волн */
.logo.animated .logo-mark path:last-of-type {
  animation: waveFlow 2s ease-in-out infinite;
}

@keyframes waveFlow {
  0%, 100% { opacity: 0.3; transform: translateY(0); }
  50% { opacity: 0.8; transform: translateY(2px); }
}

.logo:hover .logo-mark {
  transform: scale(1.02);
  filter: drop-shadow(0 0 8px rgba(0, 196, 154, 0.5));
}
</style>