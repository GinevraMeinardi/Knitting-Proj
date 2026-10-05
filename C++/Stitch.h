
#ifndef STITCH_H
#define STITCH_H

#include <iostream>
#include <optional>
#include <cmath>
#include <numbers>

class Stitch {

public:
    Stitch(float needle_size, float g_h, float tension = 1.0f);
    float GetNeedleSize() { return fSize;};
    virtual float YarnLength() const;          // st_type = K,P, m1L, m1R, K2tog....
    virtual ~Stitch() = default;
protected:
    float fSize;
    float fGh;
    float fT;
};

// ______________ Knit ___________________
class K : public Stitch {

public:
    using Stitch :: Stitch;
};
// _______________ Purl ____________________

class P : public Stitch {

public:
    using Stitch :: Stitch;
};
// _______________ Slip knot ___________________

class SlipKnot : public Stitch {

public:
    SlipKnot(float needle_size, float yarn_size, float tension = 1.0f);
    float YarnLength() const override;

private:
    float fYarnSize;
};
// _______________ Cast on ___________________

class CastOn : public Stitch {

public:
    CastOn(float needle_size, float yarn_size, float tension = 1.0f);           // constructor
    float YarnLength() const override = 0;
    virtual float CO_sts_in_length(float yarn_length_to_use) const = 0;
    virtual float CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const = 0;
    float GetNeedleSize() { return fSize;};
    float GetYarnSize() { return fYarnSize;};
    virtual ~CastOn() = default;

protected:
    float fYarnSize;
};

class LongTail_CO : public CastOn{

public:
    LongTail_CO(float needle_size, float yarn_size, float tension = 1.0f);
    float YarnLength() const override;
    float GetTailLength() const;
    float GetWorkingYarnLength() const;
    float CO_sts_in_length(float yarn_length_to_use) const override;
    float CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const override;
};

class Thumb_CO : public CastOn{

public:  
    Thumb_CO(float needle_size, float yarn_size, float tension = 1.0f);
    float YarnLength() const override;
    float CO_sts_in_length(float yarn_length_to_use) const override;
    float CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const override;
};

class Cable_CO : public CastOn{

public:
    Cable_CO(float needle_size, float yarn_size, float tension = 1.0f);
    float YarnLength() const override;
    float CO_sts_in_length(float yarn_length_to_use) const override;
    float CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const override;
};

class GermanTwist_CO : public CastOn{

public:
    GermanTwist_CO(float needle_size, float yarn_size, float tension = 1.0f);
    float YarnLength() const override;
    float CO_sts_in_length(float yarn_length_to_use) const override;
    float CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const override;
};

class Figure8_CO : public CastOn{

public:
    Figure8_CO(float needle_size, float yarn_size, float tension = 1.0f);
    float YarnLength() const override;
    float CO_sts_in_length(float yarn_length_to_use) const override;
    float CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const override;
};

class Italian_CO : public CastOn{

public:
    Italian_CO(float needle_size, float yarn_size, float tension = 1.0f);
    float YarnLength() const override;
    float CO_sts_in_length(float yarn_length_to_use) const override;
    float CO_sts_in_length(float yarn_length_to_use, float needle_size, float yarn_size) const override;
};


// _______________ Cast off ___________________

class CastOff : public Stitch {

public:
    CastOff(float needle_size, float yarn_size, float tension = 1.0f);

protected:
    float fSize;
    float fYarnSize;
    float fT;
};



#endif