var __init_gauge__ = function(mountPoint, sensor_max_val, sensor_min_val, sensor_data, sensor_unit) {
	var arcStroke = 6;
	var lineStroke = 3;
	var tickStroke = 2;
	var tickLength = 5;
	var lineColor = '#025D8C';
	var arcColor = '#1693A5';
	var valueColor = '#025D8C';
	var timestampColor = valueColor;
	var unitColor = '#1693A5';
	var tickColor = '#107FC9';
	var tickTextColor = '#1693A5';
	var tickTextSize = 11;
	var lineCap = 'round';
	var arcCap = '';
	var fontFamily = 'ibm-plex-sans,Helvetica Neue,Arial,sans-serif';
	var dangerColor = '#F26C4F';
	var inDanger = sensor_data.value > sensor_max_val || sensor_data.value < sensor_min_val;
	var lineOffset = 0;

	if (inDanger) {
    lineColor = valueColor = unitColor = dangerColor;
    if (sensor_data.value > sensor_max_val) {
    	lineOffset = ((sensor_data.value - sensor_max_val) / (sensor_max_val - sensor_min_val));
    } else {
    	lineOffset = ((sensor_min_val - sensor_data.value) / (sensor_min_val - sensor_max_val));
    }
  }

	var Shape = F2.Shape;
	var data = [{
	  pointer: sensor_unit,
	  value: sensor_data.value,
	  length: 2,
	  y: 1.05 - .05
	}];

	Shape.registerShape('point', 'dashBoard', {
	  getPoints: function getPoints(cfg) {
	    var x = cfg.x - lineOffset;
	    var y = cfg.y;

	    return [{
	      x: x,
	      y: y
	    }, {
	      x: x,
	      y: 0.4
	    }];
	  },
	  draw: function draw(cfg, container) {
	    var point1 = cfg.points[0];
	    var point2 = cfg.points[1];
	    point1 = this.parsePoint(point1);
	    point2 = this.parsePoint(point2);

	    var line = container.addShape('Polyline', {
	      attrs: {
	        points: [point1, point2],
	        stroke: lineColor,
	        lineWidth: lineStroke,
	        lineCap: ''
	      }
	    });

	    var text = cfg.origin._origin.value.toString();
	    var text1 = container.addShape('Text', {
	      attrs: {
	        text: text,
	        x: cfg.center.x,
	        y: cfg.center.y,
	        fill: valueColor,
	        fontFamily: fontFamily,
	        fontSize: 26,
	        fontWeight: 700,
	        textAlign: 'center',
	        textBaseline: 'bottom'
	      }
	    });
	    var text2 = container.addShape('Text', {
	      attrs: {
	        text: cfg.origin._origin.pointer,
	        x: cfg.center.x,
	        y: cfg.center.y,
	        fillStyle: unitColor,
	        fontFamily: fontFamily,
	        fontSize: 13,
	        textAlign: 'center',
	        textBaseline: 'top'
	      }
	    });

	    return [line, text1, text2];
	  }
	});

	var chart = new F2.Chart({
	  id: mountPoint,
	  animate: true,
	  pixelRatio: window.devicePixelRatio
	});
	chart.source(data, {
	  value: {
	    type: 'linear',
	    min: sensor_min_val,
	    max: sensor_max_val,
	    ticks: [sensor_min_val, (sensor_min_val+sensor_max_val)/2, sensor_max_val],
	    nice: false
	  },
	  length: {
	    type: 'linear',
	    min: sensor_min_val,
	    max: sensor_max_val
	  },
	  y: {
	    type: 'linear',
	    min: 0,
	    max: 1
	  }
	});

	chart.coord('polar', {
	  inner: 0,
	  startAngle: -1.25 * Math.PI,
	  endAngle: 0.25 * Math.PI
	});

	chart.axis('value', {
	  tickLine: {
	    strokeStyle: tickColor,
	    lineWidth: tickStroke,
	    length: -tickLength
	  },
	  label: null,
	  grid: null,
	  line: null
	});

	chart.axis('y', false);

	chart.guide().arc({
	  start: [sensor_min_val, 1.05],
	  end: [sensor_max_val, 1.05],
	  style: {
	    strokeStyle: arcColor,
	    lineWidth: arcStroke,
	    lineCap: arcCap
	  }
	});

	chart.guide().text({
	  position: [sensor_min_val - .5, 1.25],
	  content: String(sensor_min_val),
	  style: {
	    fillStyle: tickTextColor,
	    fontFamily: fontFamily,
	    textAlign: 'center',
	    fontSize: tickTextSize,
	  }
	});
	chart.guide().text({
	  position: [(sensor_min_val+sensor_max_val)/2, 0.75],
	  content: String((sensor_min_val+sensor_max_val)/2),
	  style: {
	    fillStyle: tickTextColor,
	    fontFamily: fontFamily,
	    textAlign: 'center',
	    fontSize: tickTextSize,
	  },
	});

	chart.guide().text({
	  position: ['90%', '-5%'],
	  content: '@ ' + sensor_data.timestamp,
	  style: {
	    fillStyle: timestampColor,
	    fontFamily: fontFamily,
	    textAlign: 'center',
	    fontSize: tickTextSize,
	  },
	});

	chart.guide().text({
	  position: [sensor_max_val + .5, 1.25],
	  content: String(sensor_max_val),
	  style: {
	    fillStyle: tickTextColor,
	    fontFamily: fontFamily,
	    textAlign: 'center',
	    fontSize: tickTextSize,
	  }
	});

	chart.point().position('value*y').size('length').color('#1890FF').shape('dashBoard');
	chart.render();
}
