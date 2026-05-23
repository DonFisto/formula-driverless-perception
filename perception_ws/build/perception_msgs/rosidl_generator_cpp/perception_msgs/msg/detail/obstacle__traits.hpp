// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from perception_msgs:msg/Obstacle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "perception_msgs/msg/obstacle.hpp"


#ifndef PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__TRAITS_HPP_
#define PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "perception_msgs/msg/detail/obstacle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace perception_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Obstacle & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: sx
  {
    out << "sx: ";
    rosidl_generator_traits::value_to_yaml(msg.sx, out);
    out << ", ";
  }

  // member: sy
  {
    out << "sy: ";
    rosidl_generator_traits::value_to_yaml(msg.sy, out);
    out << ", ";
  }

  // member: yaw
  {
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Obstacle & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: sx
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sx: ";
    rosidl_generator_traits::value_to_yaml(msg.sx, out);
    out << "\n";
  }

  // member: sy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sy: ";
    rosidl_generator_traits::value_to_yaml(msg.sy, out);
    out << "\n";
  }

  // member: yaw
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "yaw: ";
    rosidl_generator_traits::value_to_yaml(msg.yaw, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Obstacle & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace perception_msgs

namespace rosidl_generator_traits
{

[[deprecated("use perception_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const perception_msgs::msg::Obstacle & msg,
  std::ostream & out, size_t indentation = 0)
{
  perception_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use perception_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const perception_msgs::msg::Obstacle & msg)
{
  return perception_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<perception_msgs::msg::Obstacle>()
{
  return "perception_msgs::msg::Obstacle";
}

template<>
inline const char * name<perception_msgs::msg::Obstacle>()
{
  return "perception_msgs/msg/Obstacle";
}

template<>
struct has_fixed_size<perception_msgs::msg::Obstacle>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<perception_msgs::msg::Obstacle>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<perception_msgs::msg::Obstacle>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__TRAITS_HPP_
