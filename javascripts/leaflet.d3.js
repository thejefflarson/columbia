L.TileLayer.d3_geoJSON = L.TileLayer.extend({
  onAdd : function(map) {
    this.target = new L.geoJson({"type": "LineString","coordinates":[[0,0],[0,0]]}).addTo(map);
    L.TileLayer.prototype.onAdd.call(this,map);
    this._path = d3.geoPath().projection(function(d) {
      var point = map.latLngToLayerPoint(new L.LatLng(d[1],d[0]));
      return [point.x,point.y];
    });
    this.on("tileunload",function(d) {
      if (d.tile.xhr) d.tile.xhr.abort();
      if (d.tile.nodes) d.tile.nodes.remove();
      d.tile.nodes = null;
      d.tile.xhr = null;
    });
  },

  createTile: function(coords, done) {
    var tile = {};
    this._loadTile(tile, coords, done);
    return tile;
  },

  _loadTile : function(tile, tilePoint, done) {
    var self = this;
//    this._adjustTilePoint(tilePoint);
    if (!tile.nodes && !tile.xhr) {
      tile.xhr = d3.json(this.getTileUrl(tilePoint), function(geoJson) {
        tile.xhr = null;
        tile.nodes = d3.select(map._container).select("svg").append("g");
        tile.nodes.selectAll("path")
          .data(geoJson.features).enter()
          .append("path")
          .attr("d", self._path)
          .attr("class", self.options.class)
          .attr("style", self.options.style);
      });
    }
  }
});
