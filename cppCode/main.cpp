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

bool stitchImages(const vector<Mat>& imgs, Mat& pano) {
    Stitcher::Status status = stitcher->stitch(imgs, pano);

    if (status != Stitcher::OK)
    {
        cout << "Error: Can't stitch images\n";
        return false;
    }
    return true;
}

void saveAndDisplay(const Mat &pano, const string& adress) {
    std::stringstream ss;
    ss<<adress<<"/result.jpg";
    std::string caminho_saida = ss.str();

    imwrite(caminho_saida, pano);
    imshow("Result", pano);
    waitKey(0);
}

void loadConfig(Ptr<Stitcher>& stitcher) {
    stitcher->setPanoConfidenceThresh(0.8); // Adjust confidence threshold if necessary
    stitcher->setFeaturesFinder(ORB::create());
    stitcher->setBlender(makePtr<detail::MultiBandBlender>());

    stitcher->setRegistrationResol(0.5);
    stitcher->setSeamEstimationResol(0.1);
    stitcher->setCompositingResol(Stitcher::ORIG_RESOL);
    stitcher->setWaveCorrection(false);
    stitcher->setFeaturesFinder(ORB::create());
    stitcher->setFeaturesMatcher(makePtr<detail::BestOf2NearestMatcher>(false));
    stitcher->setBundleAdjuster(makePtr<detail::BundleAdjusterRay>());
    stitcher->setWarper(makePtr<SphericalWarper>());
    stitcher->setExposureCompensator(makePtr<detail::BlocksGainCompensator>());
    stitcher->setBlender(makePtr<detail::MultiBandBlender>());
}

int main(int argc, char *argv[])
{
    // Image paths (consider using a configuration file)
    if (argc != 4){
        std::cerr << "Uso: " << argv[0] << "<arg1> <arg2> <arg3>" << std::endl;
    }

    string img_path1 = argv[1];
    string img_path2 = argv[2];
    string diretorio_destino = argv[3];

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

    loadConfig(stitcher);

    // Stitch the images
    Mat pano;
    if (!(stitchImages(imgs, pano)))
    {
        return -1;
    }

    // Save and display the stitched image
    saveAndDisplay(pano, diretorio_destino);

    return 0;
}
