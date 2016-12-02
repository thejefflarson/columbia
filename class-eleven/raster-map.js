d3.json('durango.json', function(error, data) {
  d3.json('durango-contours.json', function(error, contours) {
    if(error) throw error;

    var durango = d3.select("#durango");

    durango.style("width", 401)
      .style("height", 623);

    var path = d3.geoPath()
          .projection(d3.geoMercator()
                      .fitSize([401, 623], data));

    durango.append('image')
      .attr("href", "durango.png")
      .attr("x", 0)
      .attr("y", 0)
      .attr("width", 401)
      .attr("height", 623);


    durango.append('path')
      .datum(contours)
      .attr('class', 'contours')
      .attr('d', path);

    durango.selectAll("path")
      .data(data.features)
      .enter()
      .append("path")
      .attr("d", path)
      .attr("class", function(it) {
        if(it.properties.MTFCC == "S1400") return "small";
        return "big";
      });
  });
});
