#include <iostream>
#include <vector>
#include "opencv2/highgui.hpp"
#include "opencv2/stitching.hpp"

using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{
    // File paths for the images
    string img_path1 = "C://Users//Server//Documents//CameraC//esquerdaCorrigida.jpeg";
    string img_path2 = "C://Users//Server//Documents//CameraC//direitaCorrigida.jpeg";

    // Read the images
    Mat img1 = imread(img_path1);
    Mat img2 = imread(img_path2);

    // Check if images are loaded successfully
    if (img1.empty() || img2.empty())
    {
        cout << "Error: Can't read one or more images/n";
        return -1;
    }

    // Array to store the images
    vector<Mat> imgs;
    imgs.push_back(img1);
    imgs.push_back(img2);

    // Create a Stitcher object
    Ptr<Stitcher> stitcher = Stitcher::create(Stitcher::PANORAMA);

    // Set stitching parameters
    stitcher->setPanoConfidenceThresh(0.8); // Adjust confidence threshold if necessary
    stitcher->setWaveCorrection(false);     // Disable wave correction if not needed

    // stitcher->setRegistrationResol(0.5);
    // stitcher->setSeamEstimationResol(0.1);
    // stitcher->setCompositingResol(Stitcher::ORIG_RESOL);
    // stitcher->setPanoConfidenceThresh(0.8);
    // stitcher->setWaveCorrection(false); // Essa liha que deixa as imagens fora de escala.
    // //stitcher->setWaveCorrectKind(detail::WAVE_CORRECT_HORIZ);

    // stitcher->setFeaturesFinder(ORB::create());
    // stitcher->setFeaturesMatcher(makePtr<detail::BestOf2NearestMatcher>(false));
    // stitcher->setBundleAdjuster(makePtr<detail::BundleAdjusterRay>());
    // stitcher->setWarper(makePtr<SphericalWarper>());
    // stitcher->setExposureCompensator(makePtr<detail::BlocksGainCompensator>());
    stitcher->setSeamFinder(makePtr<detail::VoronoiSeamFinder>());
    // stitcher->setBlender(makePtr<detail::MultiBandBlender>());
    

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
    imwrite("C:/Users/Server/Documents/CameraC/result.jpg", pano);

    // Display the stitched image
    imshow("Result", pano);
    waitKey(0);

    return 0;
}
