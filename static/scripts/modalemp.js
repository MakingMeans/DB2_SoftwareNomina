(function () {
  if (window.modalEmpLoaded) return;
  window.modalEmpLoaded = true;

  console.log("modalemp.js cargado");

  const TIPOS_DOCUMENTO = [
    { val: 'CC', label: 'Cédula de ciudadanía' },
    { val: 'CE', label: 'Cédula de extranjería' },
    { val: 'TI', label: 'Tarjeta de identidad' },
    { val: 'PP', label: 'Pasaporte' },
    { val: 'RC', label: 'Registro civil' },
  ];

  const CIUDADES = [
    { val: 'BOG', label: 'Bogotá, D.C.' },
    { val: 'MED', label: 'Medellín' },
    { val: 'CLO', label: 'Cali' },
    { val: 'BAQ', label: 'Barranquilla' },
    { val: 'CTG', label: 'Cartagena' },
    { val: 'CUN', label: 'Cúcuta' },
    { val: 'PEI', label: 'Pereira' },
    { val: 'MZL', label: 'Manizales' },
    { val: 'IBG', label: 'Ibagué' },
  ];

  const EPS_COLOMBIA = [
    { val: 'SURA', label: 'EPS SURA' },
    { val: 'SANITAS', label: 'EPS Sanitas' },
    { val: 'COOMEVA', label: 'EPS Coomeva' },
    { val: 'CAFESALUD', label: 'EPS Cafesalud' },
    { val: 'SALUD_TOTAL', label: 'EPS Salud Total' },
    { val: 'NUEVA_EPS', label: 'EPS Nueva EPS' },
    { val: 'COMPENSAR', label: 'EPS Compensar' },
  ];

  const FONDOS_PENSION = [
    { val: 'COLPENSIONES', label: 'Colpensiones (Público)' },
    { val: 'PORVENIR', label: 'Porvenir' },
    { val: 'PROTECCION', label: 'Protección' },
    { val: 'COLFONDOS', label: 'Colfondos' },
    { val: 'SKANDIA', label: 'Skandia' },
    { val: 'OLD_MUTUAL', label: 'Old Mutual' },
  ];

  function poblar(selectId, lista) {
    const $sel = $('#' + selectId);
    $sel.empty().append('<option value="">-- Seleccione --</option>');
    lista.forEach(item => {
      $sel.append($('<option>').val(item.val).text(item.label));
    });
  }

  $(document).ready(function () {
    $('#addEmployeeModal').on('show.bs.modal', function () {
      poblar('document_type', TIPOS_DOCUMENTO);
      poblar('city', CIUDADES);
      poblar('health_insurance', EPS_COLOMBIA);
      poblar('pension_fund', FONDOS_PENSION);

      $.getJSON('/api/departamentos_emp', function (data) {
        const $dep = $('#department_id');
        $dep.empty().append('<option value="">-- Seleccione --</option>');
        data.forEach(d => $dep.append($('<option>').val(d.id).text(d.name)));
      });

      $.getJSON('/api/cargos_emp', function (data) {
        const $pos = $('#position_id');
        $pos.empty().append('<option value="">-- Seleccione --</option>');
        data.forEach(c => $pos.append($('<option>').val(c.id).text(c.name)));
      });
    });

    $('#updateEmployeeModal').on('show.bs.modal', function () {
      poblar('document_type', TIPOS_DOCUMENTO);
      poblar('city', CIUDADES);
      poblar('health_insurance', EPS_COLOMBIA);
      poblar('pension_fund', FONDOS_PENSION);

      $.getJSON('/api/departamentos_emp', function (data) {
        const $dep = $('#department_id');
        $dep.empty().append('<option value="">-- Seleccione --</option>');
        data.forEach(d => $dep.append($('<option>').val(d.id).text(d.name)));
      });

      $.getJSON('/api/cargos_emp', function (data) {
        const $pos = $('#position_id');
        $pos.empty().append('<option value="">-- Seleccione --</option>');
        data.forEach(c => $pos.append($('<option>').val(c.id).text(c.name)));
      });
    });
  });

})();
