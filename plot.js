
var width = 960,
    height = 500;

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
	.linkDistance(200)
    .gravity(0.05)
	.friction(0.9)
    //.distance(200)
    .charge(-1000)
    .size([width, height]);

d3.json("res/plot.json", function(error, json) {

	force.nodes(json.nodes)
		.links(json.links)
		.start();


	
	// build the arrow.
	svg.append("svg:defs").selectAll("marker")
		.data(["end"])      // Different link/path types can be defined here
		.enter().append("svg:marker")    // This section adds in the arrows
		.attr("id", String)
		.attr("class", "marker")
		.attr("viewBox", "0 -5 10 10")
		.attr("refX", 18)
		.attr("refY", -.5)
		.attr("markerWidth", 6)
		.attr("markerHeight", 6)
		.attr("orient", "auto")
		.append("svg:path")
		.attr("d", "M0,-5L10,0L0,5");
		
	// add the links and the arrows
	var link = svg.append("svg:g").selectAll("path")
		.data(force.links())
		.enter().append("svg:line")
		.attr("class", "link")
		.attr("marker-end", "url(#end)");

	var node = svg.selectAll(".node")
		.data(json.nodes)
		.enter().append("g")
		.attr("class", "node")
		.call(force.drag);
		
	node.append("circle")
		.attr("r", 10)
		.style("fill", "#099");

	node.append("text")
		.attr("dx", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.id });

	force.on("tick", function() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });

		node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	});
});