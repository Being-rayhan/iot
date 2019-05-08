var __init__select_input__ = function(pre_sel_data, network_select_id, location_select_id, device_select_id, sensor_select_id, devi_network_select_id, devi_location_select_id) {
  function toggle(type, options, selected_id) {
    for (var i = 0; i < options.length; i++) {
      var option_id = $(options[i]).attr(type);
      if((option_id === 0 || option_id) && option_id == selected_id) {
        $(options[i]).show();
      } else {
        $(options[i]).hide();
      }
    }
  }

  function update_select(type, sel_val) {
    var options;
    if (type=='network') {
      options = $('#' + location_select_id + ' option');
    } else if (type=='location') {
      options = $('#' + device_select_id + ' option');
    } else if (type=='device') {
      options = $('#' + sensor_select_id + ' option');
    } else if (type=='devi-network') {
      options = $('#' + devi_location_select_id + ' option');
    }
    if (options) toggle(type, options, sel_val);
  }

  $('#' + network_select_id).change(function() {
    $("#" + location_select_id).val('');
    $("#" + device_select_id).val('');
    $('#' + sensor_select_id).val('');
    update_select('location');
    update_select('device');
    var sel_val = $(this).find(":selected").val();
    update_select('network', sel_val);
  });

  $("#" + location_select_id).change(function() {
    $('#' + device_select_id).val('');
    $('#' + sensor_select_id).val('');
    update_select('device');
    var sel_val = $(this).find(":selected").val();
    update_select('location', sel_val);
  });

  $('#' + devi_network_select_id).change(function() {
    $("#" + devi_location_select_id).val('');
    var sel_val = $(this).find(":selected").val();
    update_select('devi-network', sel_val);
  });


  if (pre_sel_data && pre_sel_data.network) $('#' + network_select_id).val(pre_sel_data.network);
  if (pre_sel_data && pre_sel_data.location) $('#' + location_select_id).val(pre_sel_data.location);
  if (pre_sel_data && pre_sel_data.device) $('#' + device_select_id).val(pre_sel_data.device);
  
  
  update_select('network', (pre_sel_data && pre_sel_data.network ? pre_sel_data.network : null));
  update_select('location', (pre_sel_data && pre_sel_data.location ? pre_sel_data.location : null));
  update_select('devi-network');
  update_select('devi-location');
}

  