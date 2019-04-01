import ee
import ipyleaflet
from ipyleaflet import TileLayer
from traitlets import default
from traitlets import Instance
from traitlets import Unicode

ee.Initialize()

def getTileLayerUrl(map_id):
  template = "https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}"
  return template.format(**map_id)

class TileLayerEE(ipyleaflet.TileLayer):    
    map_id = (
      ee.Image('NOAA/NGDC/ETOPO1')
        .select('bedrock')
        .sldStyle("""
          <RasterSymbolizer>\
            <ColorMap>\
              <ColorMapEntry color="#000033" quantity="-8000" label="deep" />\
              <ColorMapEntry color="#aaaaaa" quantity="-1" label="shallow" />\
              <ColorMapEntry color="#000000" quantity="0" label="Land" />\
              <ColorMapEntry color="#FFFFFF" quantity="4000" label="Land" />\
            </ColorMap>\
          </RasterSymbolizer>
        """).getMapId()
    )
    
    url = Unicode(
        "https://earthengine.googleapis.com/map/{mapid}/{{z}}/{{x}}/{{y}}?token={token}".format(**map_id)
    ).tag(sync=True)
    attribution = Unicode('Map data <a href="https://www.ngdc.noaa.gov/mgg/global/seltopo.html">NOAA</a>').tag(sync=True, o=True)


class Map(ipyleaflet.Map):
    
    default_tiles = Instance(TileLayerEE, allow_none=True)
    
    @default('default_tiles')
    def _default_tiles(self):
        return TileLayerEE()
    
    def __init__(self, **kwargs):
        super(Map, self).__init__(**kwargs)
        self.on_displayed(self._fire_children_displayed)
        if self.default_tiles is not None:
            self.layers = (self.default_tiles,)
        self.on_msg(self._handle_leaflet_event)
    
