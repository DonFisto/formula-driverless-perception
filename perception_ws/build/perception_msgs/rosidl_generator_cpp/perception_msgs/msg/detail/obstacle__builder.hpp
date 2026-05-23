// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from perception_msgs:msg/Obstacle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "perception_msgs/msg/obstacle.hpp"


#ifndef PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__BUILDER_HPP_
#define PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "perception_msgs/msg/detail/obstacle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace perception_msgs
{

namespace msg
{

namespace builder
{

class Init_Obstacle_yaw
{
public:
  explicit Init_Obstacle_yaw(::perception_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  ::perception_msgs::msg::Obstacle yaw(::perception_msgs::msg::Obstacle::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return std::move(msg_);
  }

private:
  ::perception_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_sy
{
public:
  explicit Init_Obstacle_sy(::perception_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_yaw sy(::perception_msgs::msg::Obstacle::_sy_type arg)
  {
    msg_.sy = std::move(arg);
    return Init_Obstacle_yaw(msg_);
  }

private:
  ::perception_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_sx
{
public:
  explicit Init_Obstacle_sx(::perception_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_sy sx(::perception_msgs::msg::Obstacle::_sx_type arg)
  {
    msg_.sx = std::move(arg);
    return Init_Obstacle_sy(msg_);
  }

private:
  ::perception_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_y
{
public:
  explicit Init_Obstacle_y(::perception_msgs::msg::Obstacle & msg)
  : msg_(msg)
  {}
  Init_Obstacle_sx y(::perception_msgs::msg::Obstacle::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Obstacle_sx(msg_);
  }

private:
  ::perception_msgs::msg::Obstacle msg_;
};

class Init_Obstacle_x
{
public:
  Init_Obstacle_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Obstacle_y x(::perception_msgs::msg::Obstacle::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Obstacle_y(msg_);
  }

private:
  ::perception_msgs::msg::Obstacle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::perception_msgs::msg::Obstacle>()
{
  return perception_msgs::msg::builder::Init_Obstacle_x();
}

}  // namespace perception_msgs

#endif  // PERCEPTION_MSGS__MSG__DETAIL__OBSTACLE__BUILDER_HPP_
