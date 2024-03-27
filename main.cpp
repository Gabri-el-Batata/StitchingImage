#include <iostream>
#include <vector>
#include "opencv2/highgui.hpp"
#include "opencv2/stitching.hpp"

using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{
    // File paths for the images
    string img_path1 = "C:\\Users\\Server\\Documents\\CameraC\\esquerdaCorrigida.jpeg";
    string img_path2 = "C:\\Users\\Server\\Documents\\CameraC\\direitaCorrigida.jpeg";

    // Read the images
    Mat img1 = imread(img_path1);
    Mat img2 = imread(img_path2);

    // Check if images are loaded successfully
    if (img1.empty() || img2.empty())
    {
        cout << "Error: Can't read one or more images\n";
        return -1;
    }

    // Array to store the images
    vector<Mat> imgs;
    imgs.push_back(img1);
    imgs.push_back(img2);

    // Create a Stitcher object
    Ptr<Stitcher> stitcher = Stitcher::create();

    // Set stitching parameters
    stitcher->setPanoConfidenceThresh(0.8); // Adjust confidence threshold if necessary
    stitcher->setWaveCorrection(false);     // Disable wave correction if not needed

    // Resulting stitched image
    Mat pano;

    // Stitch the images
    Stitcher::Status status = stitcher->stitch(imgs, pano);

    if (status != Stitcher::OK)
    {
        cout << "Error: Can't stitch images, status code: " << status << endl;
        return -1;
    }

    // Write the stitched image to disk
    imwrite("result.jpg", pano);

    // Display the stitched image
    imshow("Result", pano);
    waitKey(0);

    return 0;
}
