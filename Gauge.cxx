
#include <iostream>
#include <cmath>
#include <optional>
#include <numbers>
#include "Gauge.h"
#include "Shape.h"


Gauge::Gauge():
    fX(0),
    fY(0),
    fNsts(0),
    fNrows(0),
    fSize(0)
    {
        // default constructor
    }

Gauge::Gauge(float X, float Y, int Nsts, int Nrows, float needle_size):
    fX(X),
    fY(Y),
    fNsts(Nsts),
    fNrows(Nrows),
    fSize(needle_size)
    {
        // std constructor
}

float Gauge::TensionFactor(int sts_expected, int sts_actual){
    if( sts_actual <= 0){
        throw std::invalid_argument("The number of actual stitches must be greater than zero.");
    }
    return static_cast<float>(sts_expected)/static_cast<float>(sts_actual);
}

float Gauge::g_h(float X, int Nsts){
    return X/Nsts;
}

float Gauge::g_v(float Y, int Nrows){
    return Y/Nrows;
}

float Gauge::sts_in_Area(const Shape& region, float g_h, float g_v){
    return region.Area() / (g_h * g_v);
}

float Gauge::linear_rho(float Length_ball, float Mass_ball){
    return Mass_ball/Length_ball;
}

float Gauge::inWeight(float length, float rho){
    float mass = rho * length;
    return mass;
}

float Gauge::inLength(float mass, float rho){
    float length = mass / rho;
    return length;
}

float Gauge::yarn_length_required(float tot_sts, float needle_size, float tension){
    float R = needle_size/2;              // size is the needle's diameter
    float length_st = 3 * std::numbers::pi * R * tension;
    float tot_length = length_st*tot_sts;
    return tot_length;
}

float Gauge::yarn_weight_required(float total_length, float rho){
    float total_weight = total_length * rho;
    return total_weight;
}

float Gauge::sts_in_length(float needle_size, float length){
    float R = needle_size/2;
    float length_st = 3 * std::numbers::pi * R;
    float num_sts = std::floor(length / length_st);             // lets round to the lower closest integer
    return num_sts;
}

Gauge::~Gauge(){
    // default destructor
}