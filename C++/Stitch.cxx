#include <iostream>
#include <cmath>
#include <optional>
#include <numbers>
#include "Stitch.h"

Stitch :: Stitch(float needle_size, float g_h, float tension):
    fSize(needle_size),
    fGh(g_h),
    fT(tension)
    {}
float Stitch::YarnLength() const {
    float R = fSize/2;
    float length_st = (2 * std::numbers::pi * R + fGh) * fT;
    return length_st;
}

// ________ SlipKnot functions ________

SlipKnot :: SlipKnot(float needle_size, float yarn_size, float tension):
    Stitch(needle_size, 0.0f, tension),
    fYarnSize(yarn_size)
    {}

float SlipKnot::YarnLength() const {
    float R = fSize/2;
    float d = fYarnSize;
    float length_sk = std::numbers::pi *(2*R + 5*d) * fT;
    return length_sk;
}

CastOn::CastOn(float needle_size, float yarn_size, float tension):
    Stitch(needle_size, 0.0f, tension),
    fYarnSize(yarn_size)
    {}

LongTail_CO::LongTail_CO(float needle_size, float yarn_size, float tension):
    CastOn(needle_size, yarn_size, tension)             // using the constructor
    {}

float LongTail_CO::YarnLength()const {
    float totLength = GetTailLength() + GetWorkingYarnLength();
    return totLength;
}

float LongTail_CO::GetTailLength() const{
    float d = fYarnSize;
    float length_tail = d * (2 * std::numbers::pi + 1);
    return length_tail;
}

float LongTail_CO::GetWorkingYarnLength() const {
    float R = fSize/2;
    float d = fYarnSize;
    float length_WY = (2 * std::numbers::pi * R) + d * (1 + std::numbers::pi/2);
    return length_WY;
}

float LongTail_CO::CO_sts_in_length(float yarn_length_to_use) const {
    return CO_sts_in_length(yarn_length_to_use, fSize, fYarnSize); 
}

float LongTail_CO::CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const {
    float R = needle_size/2;
    float d = yarn_size;
    float num = yarn_length_to_use - std::numbers::pi * (2 * R + 5 * d);
    float den = (2 * std::numbers::pi * R) + (5.0f/2.0f * d * std::numbers::pi);
    float L = num /den + 1;
    return L;

}
