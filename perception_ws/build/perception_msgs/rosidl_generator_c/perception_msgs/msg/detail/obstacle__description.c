// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from perception_msgs:msg/Obstacle.idl
// generated code does not contain a copyright notice

#include "perception_msgs/msg/detail/obstacle__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_perception_msgs
const rosidl_type_hash_t *
perception_msgs__msg__Obstacle__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x25, 0xc0, 0xed, 0xea, 0xf2, 0x43, 0xef, 0x18,
      0xac, 0x78, 0xb4, 0x14, 0x7e, 0x85, 0xf6, 0x0f,
      0xb7, 0x85, 0x09, 0x7f, 0x61, 0x9f, 0x80, 0xf0,
      0xfd, 0x7a, 0x0b, 0x7c, 0x8e, 0xd3, 0x92, 0x35,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char perception_msgs__msg__Obstacle__TYPE_NAME[] = "perception_msgs/msg/Obstacle";

// Define type names, field names, and default values
static char perception_msgs__msg__Obstacle__FIELD_NAME__x[] = "x";
static char perception_msgs__msg__Obstacle__FIELD_NAME__y[] = "y";
static char perception_msgs__msg__Obstacle__FIELD_NAME__sx[] = "sx";
static char perception_msgs__msg__Obstacle__FIELD_NAME__sy[] = "sy";
static char perception_msgs__msg__Obstacle__FIELD_NAME__yaw[] = "yaw";

static rosidl_runtime_c__type_description__Field perception_msgs__msg__Obstacle__FIELDS[] = {
  {
    {perception_msgs__msg__Obstacle__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Obstacle__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Obstacle__FIELD_NAME__sx, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Obstacle__FIELD_NAME__sy, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Obstacle__FIELD_NAME__yaw, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
perception_msgs__msg__Obstacle__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {perception_msgs__msg__Obstacle__TYPE_NAME, 28, 28},
      {perception_msgs__msg__Obstacle__FIELDS, 5, 5},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 x\n"
  "float32 y\n"
  "float32 sx\n"
  "float32 sy\n"
  "float32 yaw\n"
  "";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
perception_msgs__msg__Obstacle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {perception_msgs__msg__Obstacle__TYPE_NAME, 28, 28},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 55, 55},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
perception_msgs__msg__Obstacle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *perception_msgs__msg__Obstacle__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
