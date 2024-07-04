#include <opencv2/opencv.hpp>

void stitchImages(const std::vector<cv::Mat> &images, const std::string &diretorio_destino)
{
    cv::Ptr<cv::Stitcher> stitcher = cv::Stitcher::create(cv::Stitcher::SCANS);
    cv::Mat pano;
    cv::Stitcher::Status status = stitcher->stitch(images, pano);

    stitcher->setPanoConfidenceThresh(0.5); // Ajustar limiar de confiança, se necessário
    stitcher->setFeaturesFinder(cv::ORB::create());
    stitcher->setBlender(cv::makePtr<cv::detail::MultiBandBlender>());

    stitcher->setRegistrationResol(0.6);
    stitcher->setSeamEstimationResol(0.1);
    stitcher->setCompositingResol(cv::Stitcher::ORIG_RESOL);
    stitcher->setWaveCorrection(false);
    stitcher->setWaveCorrectKind(cv::detail::WAVE_CORRECT_HORIZ);
    stitcher->setFeaturesFinder(cv::ORB::create());
    stitcher->setFeaturesMatcher(cv::makePtr<cv::detail::BestOf2NearestMatcher>(true));
    stitcher->setBundleAdjuster(cv::makePtr<cv::detail::BundleAdjusterRay>());
    stitcher->setWarper(cv::makePtr<cv::SphericalWarper>());
    stitcher->setExposureCompensator(cv::makePtr<cv::detail::BlocksGainCompensator>());
    stitcher->setBlender(cv::makePtr<cv::detail::MultiBandBlender>());

    if (status != cv::Stitcher::OK)
    {
        std::cerr << "Error stitching images, error code: " << status << std::endl;
        return;
    }

    std::stringstream ss;
    ss << diretorio_destino <<"/result.png";
    std::string caminho_saida = ss.str();

    cv::imwrite(caminho_saida, pano);

    cv::imshow("Panorama", pano);
    cv::waitKey(0);
}

int main(int argc, char *argv[])
{

    if (argc != 4)
    {
        std::cerr << "Uso: " << argv[0] << " <arg1> <arg2> <arg3>" << std::endl;
        return -1;
    }

    std::string img_path1 = argv[1];
    std::string img_path2 = argv[2];
    std::string diretorio_destino = argv[3];

    std::vector<cv::Mat> images;
    images.push_back(cv::imread(img_path1));
    images.push_back(cv::imread(img_path2));
    // Add more images as needed

    if (images.empty())
    {
        std::cerr << "No images to stitch!" << std::endl;
        return -1;
    }

    stitchImages(images, diretorio_destino);

    return 0;
}
