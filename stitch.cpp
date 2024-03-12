#include <iostream>
#include <fstream>
#include "opencv2/highgui/highgui.hpp"
#include <opencv2/stitching.hpp>

using namespace std;
using namespace cv;

// Global variables.
int height;
int width;
double minval, maxval;
Point minloc, maxloc;
Rect roi;
Mat res;

// Create function that finds point where overlap between two images starts. 
// Images "left_img" and "right_img" are passed in by find_overlaps function.
Point find_overlap_start(Mat left_img, Mat right_img)
{
    // Check if the sizes of images are the same.
    if (left_img.size() == right_img.size())
    {
        // Get rows columns of left image.
        height = left_img.rows;
        width = left_img.cols;

        // Copy left image to new variable.
        Mat haystack = left_img;

        // Create matrix "neddle" to be used as our "template". 
        roi.width = (left_img.size().width) / 2;
        roi.height = left_img.size().height;
        Mat needle = right_img(roi);

        // Apply template matching and store result in res.
        matchTemplate(haystack, needle, res, TM_CCORR_NORMED);
        minMaxLoc(res, &minval, &maxval, &minloc, &maxloc);

        // Return top-left coordinate where the matching starts.
        return maxloc;
    }
}

// Create vector of points where images start to overlap.
vector<Point> find_overlaps(vector<Mat> images)
{
    // Create vector of overlaps coordinates.
    vector<Point> overlap_starts;

    for (int i = 0; i != images.size() - 1; i++) 
    {
        // Find overlap start between two images.
        Point overlap = find_overlap_start(images[i], images[i + 1]);

        // Add overlap point to vector of points.
        overlap_starts.push_back(overlap);
    }

    // Return vector of "overlaping points" (top-left).
    return overlap_starts;
}

// Simple stitch, no blending, right hand slice overlays left hand slice.
Mat stitch_images(vector<Mat> images, vector<Point> overlap_starts)
{

    // Define variable to store width of the composite image.
    int total_width = 0;

    // Loop trought vector of overlaped points and calculate total_width.
    for (int i = 0; i < images.size() - 1; i++)
    {

        // overlap_starts[i, 0].x -> x coordinates of Point in overlap_starts vector.
        total_width += overlap_starts[i, 0].x;

    }

    // Now add width of image to the total width.
    int img_width = images[0].cols;
    total_width = total_width + img_width;

    // Create matrix that is of the size ( height, total_width -> depends on the number of images).
    Mat result = Mat::zeros(Size(total_width, height), CV_8UC1);

    // Put images next to each other on the result matrix.
    int current_column = 0;
    for (int i = 0; i < images.size(); i++)
    {
        // Where to copy current image?
        images[i].copyTo(result.rowRange(0,400).colRange(current_column,( current_column+600 ) ));

        // The next image should be moved right for:
        current_column += overlap_starts[i, 0].x;
    }

    // Display composite image.
    namedWindow("result", WINDOW_AUTOSIZE);
    imshow("result", result);

    return result;
}


int main(int argc, char* argv[])
{
    // Load images from HD.
    Mat img1 = imread("foto0.png", CV_LOAD_IMAGE_GRAYSCALE);
    Mat img2 = imread("foto1.png", CV_LOAD_IMAGE_GRAYSCALE);

    // Create vector of images.
    vector<Mat> various_images;
    various_images.push_back(img1);
    various_images.push_back(img2);


    // Display loaded images if you want.
    namedWindow("img1", WINDOW_AUTOSIZE);
    imshow("img1", img1);
    namedWindow("img2", WINDOW_AUTOSIZE);
    imshow("img2", img2);

    // Call function find_overlaps ( find top-left points of overlaping).
    vector<Point> overlap_starts = find_overlaps(various_images);

    // Call stitch_function and stitch images together.
    stitch_images(various_images, overlap_starts);

    waitKey(0);
    return 0;
}
