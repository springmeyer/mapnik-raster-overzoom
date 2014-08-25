

## Mapnik Raster overzoom

This testcase:

 - Renders a 256x256 final image
 - Uses a source image that is also 256x256 that is meant to represent the entire world's mercator bbox
 - Tests rendering at various extents that mimic a few tile requests
 - Uses a large buffer size to more clearly expose the problem
 - The farther you zoom in the more you overzoom on the existing raster (a pixelatted result is expect in a real world situation)

 The problem is:

 - The farther you zoom in the larger the intermediate buffer becomes that is created right here: https://github.com/mapnik/mapnik/blob/48c23f27dc1524fb17d7f81160a72cd2639d8b07/include/mapnik/renderer_common/process_raster_symbolizer.hpp#L113
 - This starts really hurting performance at higher zooms
 - Ultimately a very high zoom and very large buffer could end up allocating an image too big for the heap


Using the `debug.diff` patch against master and running the test `python test.py` gives:


```
Mapnik LOG> 2014-08-24 19:28:30: ctrans w/h 256/256
Mapnik LOG> 2014-08-24 19:28:30: ctrans scale x/y 6.38802e-06/6.38802e-06
Mapnik LOG> 2014-08-24 19:28:30: ctrans extent box2d(-20037508.3427892439067364,-20037508.3427892439067364,20037508.3427892439067364,20037508.3427892439067364)
Mapnik LOG> 2014-08-24 19:28:30: source w/h 256/256
Mapnik LOG> 2014-08-24 19:28:30: source->ext_ box2d(-20037508.3427892439067364,-20037508.3427892476320267,20037508.3427892439067364,20037508.3427892774343491)
Mapnik LOG> 2014-08-24 19:28:30: ext box2d(0.0000000000000000,-0.0000000000002142,255.9999999999999716,256.0000000000000568)
Mapnik LOG> 2014-08-24 19:28:30: raster width/height 256/256
Mapnik LOG> 2014-08-24 19:28:30: start x/y 0/0
Mapnik LOG> 2014-08-24 19:28:30: end x/y 256/256
Mapnik LOG> 2014-08-24 19:28:30: image_ratio x/y 1/1
Mapnik LOG> 2014-08-24 19:28:30: •••••••••••• SCALE 1:1 ••••••••••••
Mapnik LOG> 2014-08-24 19:28:30: •••••••••••• DIRECT COMPOSITE ••••••••••••

Mapnik LOG> 2014-08-24 19:28:30: ctrans w/h 256/256
Mapnik LOG> 2014-08-24 19:28:30: ctrans scale x/y 1.2776e-05/1.2776e-05
Mapnik LOG> 2014-08-24 19:28:30: ctrans extent box2d(-20037508.3427892439067364,0.0000000000000000,0.0000000000000000,20037508.3427892439067364)
Mapnik LOG> 2014-08-24 19:28:30: source w/h 256/256
Mapnik LOG> 2014-08-24 19:28:30: source->ext_ box2d(-20037508.3427892439067364,-20037508.3427892476320267,20037508.3427892439067364,20037508.3427892774343491)
Mapnik LOG> 2014-08-24 19:28:30: ext box2d(0.0000000000000000,-0.0000000000004284,511.9999999999999432,512.0000000000001137)
Mapnik LOG> 2014-08-24 19:28:30: raster width/height 512/512
Mapnik LOG> 2014-08-24 19:28:30: start x/y 0/0
Mapnik LOG> 2014-08-24 19:28:30: end x/y 512/512
Mapnik LOG> 2014-08-24 19:28:30: image_ratio x/y 2/2
Mapnik LOG> 2014-08-24 19:28:30: •••••••••••• TARGET TOO BIG ••••••••••••

Mapnik LOG> 2014-08-24 19:28:30: ctrans w/h 256/256
Mapnik LOG> 2014-08-24 19:28:30: ctrans scale x/y 2.55521e-05/2.55521e-05
Mapnik LOG> 2014-08-24 19:28:30: ctrans extent box2d(-20037508.3427892439067364,-0.0000000009313226,-10018754.1713946219533682,10018754.1713946200907230)
Mapnik LOG> 2014-08-24 19:28:30: source w/h 256/256
Mapnik LOG> 2014-08-24 19:28:30: source->ext_ box2d(-20037508.3427892439067364,-20037508.3427892476320267,20037508.3427892439067364,20037508.3427892774343491)
Mapnik LOG> 2014-08-24 19:28:30: ext box2d(0.0000000000000000,-256.0000000000009663,1023.9999999999998863,768.0000000000002274)
Mapnik LOG> 2014-08-24 19:28:30: raster width/height 1024/1024
Mapnik LOG> 2014-08-24 19:28:30: start x/y 0/-256
Mapnik LOG> 2014-08-24 19:28:30: end x/y 1024/768
Mapnik LOG> 2014-08-24 19:28:30: image_ratio x/y 4/4
Mapnik LOG> 2014-08-24 19:28:30: •••••••••••• TARGET TOO BIG ••••••••••••

Mapnik LOG> 2014-08-24 19:28:30: ctrans w/h 256/256
Mapnik LOG> 2014-08-24 19:28:30: ctrans scale x/y 0.0523307/0.0523307
Mapnik LOG> 2014-08-24 19:28:30: ctrans extent box2d(-166326.9735485427081585,6775378.1871980242431164,-161435.0037382915616035,6780270.1570082753896713)
Mapnik LOG> 2014-08-24 19:28:30: source w/h 2/1
Mapnik LOG> 2014-08-24 19:28:30: source->ext_ box2d(-313086.0678560808300972,6731350.4589057825505733,0.0000000000000000,6887893.4928338229656219)
Mapnik LOG> 2014-08-24 19:28:30: ext box2d(-7680.0000000001955414,-5632.0000000011696102,8704.0000000001946319,2559.9999999990254764)
Mapnik LOG> 2014-08-24 19:28:30: raster width/height 16384/8192
Mapnik LOG> 2014-08-24 19:28:30: start x/y -7680/-5632
Mapnik LOG> 2014-08-24 19:28:30: end x/y 8704/2560
Mapnik LOG> 2014-08-24 19:28:30: image_ratio x/y 8192/8192
Mapnik LOG> 2014-08-24 19:28:30: •••••••••••• TARGET TOO BIG ••••••••••••
```
