from xml.etree import ElementTree as et
 

def svg(layers,fName):
        doc = et.Element('svg', width='480', height='360', version='1.1', 
                        xmlns='http://www.w3.org/2000/svg')
  
        colDict = {
          0: 'pink',
          1: 'blue',
          2: 'green',
          3: 'red',
          4: 'grey',
          5: 'cyan',
          6: 'grey'
        }

        y0, dy = 0, 10
        dx = 30
        for no, (zRange, (c, rho, mu)) in sorted(layers.iteritems()):
            x0,x1 = zRange
            et.SubElement(doc, 'rect', x=str(x0*dx), y=str(y0), 
                            width=str((x1-x0)*dx), height=str(dy), 
                            fill=colDict[no])
   
        with open(fName, 'w') as outFile:
            outFile.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
            outFile.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
            outFile.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
            outFile.write(et.tostring(doc))
            outFile.close()

