var __init_chart__ = function(mountPoint, sensor_unit, sensor_max_val, sensor_min_val, sensor_val, sensor_values, label) {
  var data = sensor_values;
  var lineColor = '#025D8C';
  var textColor = '#1693A5';
  var lineWidth = 4;
  var fontFamily = 'ibm-plex-sans,Helvetica Neue,Arial,sans-serif';
  var dangerColor = '#F26C4F';

  if (data.length === 1) lineWidth = 6;

  getAllFreqs = function(){
    var freqs = [];
    for (var i = 0; i < data.length; i++) {
      freqs.push(data[i][label.x]);
    }
    return freqs;
  }

  var max_data = data.reduce(function(prev, current) {
    return prev.value > current.value ? prev : current;
  });

  var min_data = data.reduce(function(prev, current) {
    return prev.value < current.value ? prev : current;
  });

  var chart = new F2.Chart({
    id: mountPoint,
    pixelRatio: window.devicePixelRatio,
    padding: 50
  });


  chart.source(data, {
    [label.x]: {
      ticks: getAllFreqs()
    },
    value: {
      min: min_data.value > sensor_min_val ? sensor_min_val : min_data.value,
      max: max_data.value < sensor_max_val ? sensor_max_val : max_data.value,
    }
  });

  chart.axis(label.x, {
    label: {
      fontFamily: fontFamily,
      textAlign: 'start',
      fill: textColor
    },
    tickLine: {
      length: 5,
      stroke: textColor
    },
    line: {
      stroke: textColor,
      strokeOpacity: 0.4
    }
  });
  chart.axis(label.y, {
    label: {
      fontFamily: fontFamily,
      fill: textColor,
    },
    grid: {
      lineDash: null,
      stroke: textColor,
      strokeOpacity: 0.3
    }
  });
  chart.line().position(label.x + '*' + label.y).color(lineColor).size(lineWidth).style({lineCap:'square'});


  chart.guide().regionFilter({
    start: ['min', sensor_max_val],
    end: ['max', 'max'],
    color: dangerColor
  });

  chart.guide().regionFilter({
    start: ['min', sensor_min_val],
    end: ['max', 'min'],
    color: dangerColor
  });

  chart.guide().regionFilter({
    start: ['min', sensor_min_val],
    end: ['max', sensor_max_val],
    color: lineColor
  });
  
  // chart.guide().text({
  //   position: ['max', 50],
  //   content: 'xxxx',
  //   offsetX: -5,
  //   style: {
  //     fill: '#4BC1C2',
  //     textAlign: 'end'
  //   }
  // });

  chart.render();
}