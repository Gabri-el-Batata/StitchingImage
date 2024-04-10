#include <iostream>
#include <vector>
#include "opencv2/highgui.hpp"
#include "opencv2/stitching.hpp"

using namespace std;
using namespace cv;

Ptr<Stitcher> stitcher = Stitcher::create(Stitcher::PANORAMA); // Global Variable

bool loadImages(const string& img_path1, const string& img_path2, Mat& img1, Mat& img2) {
    img1 = imread(img_path1);
    img2 = imread(img_path2);

    if(img1.empty() || img2.empty()) {
        cout << "Error: Some image is empty.\n";
        return false;
    }

    return true;
}

// Ptr<Stitcher> createStitcher()
// {
//     Ptr<Stitcher> stitcher = Stitcher::create(Stitcher::PANORAMA);
//     stitcher->setPanoConfidenceThresh(0.8); // Adjust confidence threshold if necessary
//     stitcher->setWaveCorrection(false);     // Disable wave correction if not needed
//     //stitcher->setSeamFinder(makePtr<detail::VoronoiSeamFinder>());

//     //Optional stitcher configuration (uncomment if needed)
//     //stitcher->setRegistrationResol(0.5);
//     //stitcher->setSeamEstimationResol(0.1);
//     //stitcher->setCompositingResol(Stitcher::ORIG_RESOL);
//     //stitcher->setWaveCorrection(false); // Essa liha que deixa as imagens fora de escala.
//     ////stitcher->setWaveCorrectKind(detail::WAVE_CORRECT_HORIZ);
//     //stitcher->setFeaturesFinder(ORB::create());
//     //stitcher->setFeaturesMatcher(makePtr<detail::BestOf2NearestMatcher>(false));
//     //stitcher->setBundleAdjuster(makePtr<detail::BundleAdjusterRay>());
//     //stitcher->setWarper(makePtr<SphericalWarper>());
//     //stitcher->setExposureCompensator(makePtr<detail::BlocksGainCompensator>());
//     //stitcher->setBlender(makePtr<detail::MultiBandBlender>());

//     return stitcher;
// }



bool stitchImages(const vector<Mat>& imgs, Mat& pano) {
    Stitcher::Status status = stitcher->stitch(imgs, pano);

    if (status != Stitcher::OK)
    {
        cout << "Error: Can't stitch images\n";
        return false;
    }
    return true;
}

void saveAndDisplay(const Mat &pano)
{
    imwrite("C:/Users/Server/Documents/CameraC/result.jpg", pano);
    imshow("Result", pano);
    waitKey(0);
}

int main(int argc, char *argv[])
{
    // Image paths (consider using a configuration file)
    string img_path1 = "C://Users//Server//Documents//CameraC//esquerdaCorrigida.jpeg";
    string img_path2 = "C://Users//Server//Documents//CameraC//direitaCorrigida.jpeg";

    // Load images
    Mat img1, img2;
    if (!loadImages(img_path1, img_path2, img1, img2))
    {
        return -1;
    }

    // Create a vector of images
    vector<Mat> imgs;
    imgs.push_back(img1);
    imgs.push_back(img2);

    // Configuritaions of the process of stitching
    stitcher->setPanoConfidenceThresh(0.8); // Adjust confidence threshold if necessary
    stitcher->setWaveCorrection(false);     // Disable wave correction if not needed

    stitcher->setRegistrationResol(0.5);
    stitcher->setSeamEstimationResol(0.1);
    stitcher->setCompositingResol(Stitcher::ORIG_RESOL);
    stitcher->setWaveCorrection(false); // Essa liha que deixa as imagens fora de escala.
    stitcher->setFeaturesFinder(ORB::create());
    stitcher->setFeaturesMatcher(makePtr<detail::BestOf2NearestMatcher>(false));
    stitcher->setBundleAdjuster(makePtr<detail::BundleAdjusterRay>());
    stitcher->setWarper(makePtr<SphericalWarper>());
    stitcher->setExposureCompensator(makePtr<detail::BlocksGainCompensator>());
    stitcher->setBlender(makePtr<detail::MultiBandBlender>());

    // Stitch the images
    Mat pano;
    if (!(stitchImages(imgs, pano)))
    {
        return -1;
    }

    // Save and display the stitched image
    saveAndDisplay(pano);

    return 0;
}
