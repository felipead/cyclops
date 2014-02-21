#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>

using namespace std;
using namespace cv;

void match(Mat& referenceImage, Mat& templateImage, Mat& matchResult, int numberOfTimesToMatch, Scalar hightLightColor) {
    Mat grayReferenceImage, grayTemplateImage;
    cvtColor(referenceImage, grayReferenceImage, CV_BGR2GRAY);
    cvtColor(templateImage, grayTemplateImage, CV_BGR2GRAY);

    matchTemplate(grayReferenceImage, grayTemplateImage, matchResult, CV_TM_CCOEFF_NORMED);
    normalize(matchResult, matchResult, 0, 1, NORM_MINMAX, -1);
    threshold(matchResult, matchResult, 0.5, 1, CV_THRESH_TOZERO);

    for (int i = 0; i < numberOfTimesToMatch; i++) {
        double minValue, maxValue;
        cv::Point minLocation, maxLocation;
        cv::minMaxLoc(matchResult, &minValue, &maxValue, &minLocation, &maxLocation);

        cv::rectangle(
            referenceImage,
            maxLocation, 
            cv::Point(maxLocation.x + templateImage.cols, maxLocation.y + templateImage.rows),
            hightLightColor, 2
        );
        cv::floodFill(matchResult, maxLocation, Scalar(0), 0, Scalar(.1), Scalar(1.));
    }
}

int main(int argumentCount, char* arguments[]) {
    if (argumentCount != 6)  {
        return -1;
    }
    Mat circleTemplate1 = cv::imread(arguments[1]);
    Mat circleTemplate2 = cv::imread(arguments[2]);
    Mat ballTemplate1 = cv::imread(arguments[3]);
    Mat ballTemplate2 = cv::imread(arguments[4]);
    Mat referenceImage = cv::imread(arguments[5]);
    if (referenceImage.empty() || circleTemplate1.empty() || circleTemplate2.empty() || ballTemplate1.empty() || ballTemplate2.empty()) {
        return -1;
    }

    Mat circleMatchResult1(referenceImage.rows - circleTemplate1.rows + 1, referenceImage.cols - circleTemplate1.cols + 1, CV_32FC1);
    match(referenceImage, circleTemplate1, circleMatchResult1, 3, CV_RGB(0,255,0));

    Mat circleMatchResult2(referenceImage.rows - circleTemplate2.rows + 1, referenceImage.cols - circleTemplate2.cols + 1, CV_32FC1);
    match(referenceImage, circleTemplate2, circleMatchResult2, 3, CV_RGB(0,255,255));

    Mat ballMatchResult1(referenceImage.rows - ballTemplate1.rows + 1, referenceImage.cols - ballTemplate1.cols + 1, CV_32FC1);
    match(referenceImage, ballTemplate1, ballMatchResult1, 1, CV_RGB(255,0,0));

    Mat ballMatchResult2(referenceImage.rows - ballTemplate2.rows + 1, referenceImage.cols - ballTemplate2.cols + 1, CV_32FC1);
    match(referenceImage, ballTemplate2, ballMatchResult2, 1, CV_RGB(255,255,0));
    
    imshow("reference image", referenceImage);
    waitKey();
    return 0;
}