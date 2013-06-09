
var width = 1024,
    height = 720;
	
var color = d3.scale.category10();

var svg = d3.select("#chart").append("svg")
	.attr("xmlns", "http://www.w3.org/2000/svg")
    .attr("width", width)
    .attr("height", height);


var force = d3.layout.force()
	.linkDistance(150)
    .gravity(0.05)
	.friction(0.9)
    .charge(-800)
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
	var link = svg.selectAll(".line")
		.data(force.links())
		.enter().append("line")
		.attr("class", "link")
		.attr("marker-end", "url(#end)")
		.style("fill", "#036")
		.style("stroke", "#036")
		.style("stroke-width", "2px");

	var node = svg.selectAll(".node")
		.data(json.nodes)
		.enter().append("g")
		.attr("class", "node")
		
		.call(force.drag);
		
	node.append("circle")
		.attr("r", 10)
		.on("click", click)
		.style("fill", function(d) { return color(d.group); });

	node.append("text")
		.attr("dx", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.id.substr(7)});

	force.on("tick", function() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });

		node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	});
});

d3.select("#download").on("click", function(){
		d3.select(this)
        .attr("href", 'data:application/octet-stream;base64,' + btoa(d3.select("#chart").html()))
        .attr("download", "viz.svg") 
    })
	
function click (d){
	d3.select(this).attr('r', 15)
	.style("fill","lightcoral")
	.style("stroke","red")
	d.id
	window.location = d.id
}