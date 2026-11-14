// Print face landmarks of a photo as JSON, in image pixels with the origin at the top left. Runs on this Mac (Apple Vision).
// Usage: swift face_landmarks.swift photo.png
import Foundation
import Vision
import CoreImage
let input = CIImage(contentsOf: URL(fileURLWithPath: CommandLine.arguments[1]))!
let size = input.extent.size
let req = VNDetectFaceLandmarksRequest()
try VNImageRequestHandler(ciImage: input).perform([req])
guard let f = req.results?.first, let l = f.landmarks else { print("{}"); exit(1) }
var out: [String: [[Double]]] = [:]
let parts: [(String, VNFaceLandmarkRegion2D?)] = [("lips", l.outerLips), ("left_brow", l.leftEyebrow), ("right_brow", l.rightEyebrow), ("left_eye", l.leftEye), ("right_eye", l.rightEye), ("nose", l.nose)]
for (n, r) in parts { if let r = r { out[n] = r.pointsInImage(imageSize: size).map { [Double($0.x), Double(size.height) - Double($0.y)] } } }
let b = f.boundingBox
out["box"] = [[Double(b.minX * size.width), Double((1 - b.maxY) * size.height)], [Double(b.maxX * size.width), Double((1 - b.minY) * size.height)]]
print(String(data: try JSONSerialization.data(withJSONObject: out), encoding: .utf8)!)
