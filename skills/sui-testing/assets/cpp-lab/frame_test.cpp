#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

static std::string decode(const std::string& packet) {
    if (packet.empty()) throw std::invalid_argument("empty frame");
    const auto size = static_cast<unsigned char>(packet[0]);
    if (size > 64 || packet.size() != static_cast<std::size_t>(size) + 1)
        throw std::invalid_argument("invalid length");
    return packet.substr(1);
}
TEST(Frame, PreservesEmptyPayload) { EXPECT_EQ(decode(std::string(1, '\0')), ""); }
TEST(Frame, RejectsTruncatedPayload) { EXPECT_THROW(decode(std::string("\x02" "a", 2)), std::invalid_argument); }
TEST(Frame, PreservesBinaryPayload) { EXPECT_EQ(decode(std::string("\x02\0x", 3)), std::string("\0x", 2)); }
