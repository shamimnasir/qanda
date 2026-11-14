// Cut the person out of a photo with Apple's on-device Vision subject mask. Nothing leaves the Mac.
// Usage: ./studio.sh cutout in.jpg out.png
import Foundation
import Vision
import CoreImage
let a = CommandLine.arguments
guard a.count == 3 else { print("usage: cutout in out.png"); exit(2) }
let input = CIImage(contentsOf: URL(fileURLWithPath: a[1]))!
let handler = VNImageRequestHandler(ciImage: input)
let req = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([req])
guard let r = req.results?.first else { print("no subject found"); exit(1) }
let buf = try r.generateMaskedImage(ofInstances: r.allInstances, from: handler, croppedToInstancesExtent: false)
let ctx = CIContext()
try ctx.writePNGRepresentation(of: CIImage(cvPixelBuffer: buf), to: URL(fileURLWithPath: a[2]), format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!)
print("ok")
