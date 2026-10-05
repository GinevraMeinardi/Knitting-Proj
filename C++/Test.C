
// Test macro

#include <iostream>
#include <optional>
#include <cmath>
#include <numbers>
#include "Swatch.h"
#include "Shape.h"
#include "Stitch.h"


int main(){
    float needle_size = 6;      // mm
    float target_sts = 10;      // 10 stitches
    float target_L = 200;      // mm
    // calculate the actual gauge
    Swatch testSwatch(7,2,10,4,needle_size);              // 7 and 2 cm, 10 sts, 4 rows, 6mm needles
    float g_v = testSwatch.g_v();
    float g_h = testSwatch.g_h();
    // float ball_weight = 
    testSwatch.setWeight(100);    // g
    // float ball_length = 
    testSwatch.setLength(150);    // m
    
    K knit_st(needle_size, g_h);
    
    
    std::cout << std::endl << "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV" << std::endl;
    std::cout << "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV Knitting Calculator VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV" << std::endl;
    std::cout << "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV" << std::endl << std::endl;
    std::cout << "your average stitch is " << g_v << "cm high. (g_v)" << std::endl;
    std::cout << "your average stitch is " << g_h << "cm wide. (g_h)" << std::endl;
    
    float lin_density = testSwatch.linear_rho(testSwatch.getWeight().value(), testSwatch.toMillimiters(testSwatch.getLength().value()));
    // float lin_density = testSwatch.linear_rho(ball_weight, ball_length);                // 100g, 150m

    std::cout << std::endl << "which gives us an approximate linear density of " << lin_density << " g/mm."<< std::endl;
    
    // knowing the linear density, I can calculate how much 1m of yarn weights
    float mass_1m = testSwatch.inWeight(target_L, lin_density);

    // std::cout << "Therefore, " << Swatch::toMeters(target_L) <<"m of this yarn should weight " << mass_1m << "g." << std::endl;

    std::cout << std::endl << "The theoretical (geometrical) length needed to knit " <<  target_sts << " stitches on a " << knit_st.GetNeedleSize() << "mm needle is " << std::endl;
    // calculate the length corresponding to an increasing number of stitches sts
    float arr[7]; // target_sts*knit_st.YarnLength();
    float oldArr[7];
    float realArr[7] = {130, 266, 398, 526, 653, 777, 898};

    for(int i = 0; i < 7; i++){
        int n = (i+1)*5;
        arr[i] = n * knit_st.YarnLength();
        oldArr[i] = n* 3 * std::numbers::pi * needle_size/2;

        std::cout << "n = " << n << " | length = " << arr[i] << " | realLength " << realArr[i] << " | Old " << oldArr[i] << std::endl;
        std::cout  << std::endl << "delta real-arr " << realArr[i] - arr[i] << " mm." << std::endl; 
        std::cout << "delta real-old " << realArr[i] - oldArr[i] << " mm." << std::endl; 
    }
/*    
    float estimated_mass_10sts = testSwatch.inWeight(estimated_length_10sts, lin_density);            
    std::cout << "Thus the corresponding estimated weight for such length is " << estimated_mass_10sts << " g." << std::endl;

    // calculate how many stitches there should be in 1m based off you gauge
    float sts_in_1m = testSwatch.sts_in_length(target_L);              
    std::cout << std::endl << "Based on your gauge, in " << Swatch::toMeters(target_L) << "m of yarn there should be " << sts_in_1m << " stitches." << std::endl; 
    // float estimated_length_in1m = testSwatch.yarn_length_required(sts_in_1m);
    // std::cout << std::endl << "The theoretical (geometrical) length needed to knit " <<  sts_in_1m << " stitches on a " << testSwatch.getNeedle_size() << "mm needle is " << testSwatch.toMeters(estimated_length_in1m) << "m." << std::endl;

    // define the tension factor
    float T = testSwatch.TensionFactor_sts(target_sts,sts_in_1m);
    std::cout << std::endl << "The tension factor to consider to match your swatch with the geometrical approximation swatch is " << T << "." <<std::endl;
    float T2 = testSwatch.TensionFactor_len(Swatch::toMeters(estimated_length_37sts), 0.18);              // my actual measurement is 18cm
    std::cout << std::endl << "I could also calculate that using the yarn length used. In this case the tension factor is " << T2 << std::endl;
    if(T2 < 1){
        std::cout << "You're a tight knitter!" << std::endl;
    }
    else std::cout << "You're a loose knitter!" << std::endl;
    
    // estimate how many stitches there are in 100g with that gauge with and w/o the tension factor
    float length_100g = testSwatch.inLength(100, lin_density);
    float sts_in_100g = testSwatch.sts_in_length(length_100g);
    float sts_in_100g_wT = testSwatch.sts_in_length(length_100g, T);
    std::cout << "Without tension, in 100g of yarn you should be able to knit " << sts_in_100g << " stitches."; 
    std::cout << " Considering the tension factor, you should be able to knit " << sts_in_100g_wT << " stitches." << std::endl;

    std::cout << "___________________________________________________________________________________________________" << std::endl;
    std::cout << "Let's recalculate everything using data on yarn label:" << std::endl;
    std::cout << "___________________________________________________________________________________________________" << std::endl;

    // let's calculate with respect to the suggested gauge
    Swatch labelSwatch(10, 10, 14, 21, 6);
    float g_v_label = labelSwatch.g_v();
    float g_h_label = labelSwatch.g_h();

    std::cout << "The average stitch is " << g_v_label << "cm high." << std::endl;
    std::cout << "The average stitch is " << g_h_label << "cm wide." << std::endl;

    // how big is the area you'd cover with 10stsx10rows
    float Area_covered_mygauge = testSwatch.Area_in_sts(10, 10, g_h, g_v);
    float Area_covered_labelgauge = labelSwatch.Area_in_sts(10, 10, g_h_label, g_v_label);

    std::cout << "With a swatch of 10 sts x 10 rows, in your gauge you'd cover an area of " << Area_covered_mygauge << " cm^2." << std::endl;
    std::cout << "In the suggested gauge, you'd cover an area of " << Area_covered_labelgauge << " cm^2." << std::endl;

    Rectangle swatchShape(10,10);           // 10cm x 10cm
    float sts_1010swatch_mygauge = testSwatch.sts_in_Area(swatchShape, g_h, g_v);
    float sts_1010swatch_labelgauge = labelSwatch.sts_in_Area(swatchShape, g_h_label, g_v_label);

    std::cout << "To knit a swatch of 10 cm x 10 cm, in your gauge you'd need " << sts_1010swatch_mygauge << " stitches." << std::endl;
    std::cout << "In the suggested gauge, you'd need " << sts_1010swatch_labelgauge << " stitches." << std::endl;
*/

    return 0;   
}
