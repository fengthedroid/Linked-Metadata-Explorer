var w = 700,
	h = 500,
	fill = d3.scale.category20();
	
var vis = d3.select("#chart")
	.append("svg:svg")
	.attr("width", w)
	.attr("height", h);
	
var force = d3.layout.force()
    .gravity(.0)
    .distance(500)
    .charge(-100)
    .size([w, h]);
	
d3.json("res/plot.json", function(json) {
	var force = d3.layout.force()
	    .charge(-120)
	    .linkDistance(200)
	    .nodes(json.nodes)
	    .links(json.links)
		.size([w, h])
	    .start();
	
	var link = vis.selectAll("line.link")
	    .data(json.links)
	    .enter().append("svg:line")
	    .attr("class", "link")
	    .style("stroke-width", function(d) { return Math.sqrt(d.value); })
	    .attr("x1", function(d) { return d.source.x; })
	    .attr("y1", function(d) { return d.source.y; })
	    .attr("x2", function(d) { return d.target.x; })
	    .attr("y2", function(d) { return d.target.y; });
		

	
	var node = vis.selectAll(".node")
	    .data(json.nodes)
		.enter().append("g")
		.attr("class", "node")
		.call(force.drag)
		//.append("text").text(function(d) { return d.id })
	    .append("svg:circle")	
	    .attr("cx", function(d) { return d.x; })
	    .attr("cy", function(d) { return d.y; })
	    .attr("r", 13)
	    .style("fill", function(d) { return fill(d.group); });
	    

	vis.style("opacity", 1e-6)
	    .transition()
	    .duration(1000)
	    .style("opacity", 1);
	
	force.on("tick", function() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	
		node.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });
	});
});