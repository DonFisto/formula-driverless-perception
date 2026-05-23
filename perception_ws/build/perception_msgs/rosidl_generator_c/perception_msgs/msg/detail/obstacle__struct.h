// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from perception_msgs:msg/Obstacle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "perception_msgs/msg/obstacle.h"


#ifndef PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__STRUCT_H_
#define PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/Obstacle in the package perception_msgs.
typedef struct perception_msgs__msg__Obstacle
{
  float x;
  float y;
  float sx;
  float sy;
  float yaw;
} perception_msgs__msg__Obstacle;

// Struct for a sequence of perception_msgs__msg__Obstacle.
typedef struct perception_msgs__msg__Obstacle__Sequence
{
  perception_msgs__msg__Obstacle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} perception_msgs__msg__Obstacle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__STRUCT_H_
