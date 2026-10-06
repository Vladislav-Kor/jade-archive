// test_partners.js
// Вставьте этот код в консоль браузера (F12) для тестирования

console.log('🧪 Тестирование открытия PartnerModal');

// Находим компоненты
const app = document.querySelector('.app').__vueParentComponent;
const ctx = app.ctx;

console.log('📋 Доступные методы:');
console.log('  openPartnerModal:', typeof ctx.openPartnerModal);
console.log('  openModal:', typeof ctx.openModal);
console.log('  partnerModalRef:', ctx.partnerModalRef);

// Пытаемся открыть модалку
console.log('🚀 Пытаемся открыть PartnerModal...');
try {
    ctx.openPartnerModal(null, 1);
    console.log('✅ openPartnerModal вызван успешно');
} catch (err) {
    console.error('❌ Ошибка при вызове openPartnerModal:', err);
}

// Проверяем ref
console.log('🔍 partnerModalRef.value:', ctx.partnerModalRef?.value);
if (ctx.partnerModalRef?.value) {
    console.log('✅ partnerModalRef существует');
    console.log('  Методы:', Object.keys(ctx.partnerModalRef.value));
} else {
    console.log('❌ partnerModalRef НЕ СУЩЕСТВУЕТ!');
}
