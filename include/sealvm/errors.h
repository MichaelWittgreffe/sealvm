#ifndef SEALVM_SEALVM_ERRORS_H
#define SEALVM_SEALVM_ERRORS_H

typedef enum ErrCode {
    NO_ERR,
    THIS_IS_NULL,
    ADDRESS_OUT_OF_BOUNDS,
    DEVICE_TYPE_NOT_SUPPORTED,
    DEVICE_FUNCTION_NOT_SUPPORTED,
    DEVICE_IS_NULL,
    CANNOT_CONSTRUCT,
    REGION_NOT_FOUND,
    CANNOT_COMPUTE_HASH,
    INVALID_REGISTER,
} ErrCode;

#endif // SEALVM_SEALVM_ERRORS_H