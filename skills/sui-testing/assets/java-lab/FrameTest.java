import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class FrameTest {
    static byte[] decode(byte[] packet) {
        if (packet == null || packet.length == 0) throw new IllegalArgumentException("empty frame");
        int length = Byte.toUnsignedInt(packet[0]);
        if (length > 64 || packet.length != length + 1) throw new IllegalArgumentException("invalid length");
        return java.util.Arrays.copyOfRange(packet, 1, packet.length);
    }
    @Test void emptyPayload() { assertArrayEquals(new byte[0], decode(new byte[]{0})); }
    @Test void truncatedPayload() { assertThrows(IllegalArgumentException.class, () -> decode(new byte[]{2, 1})); }
    @Test void binaryPayload() { assertArrayEquals(new byte[]{0, 1}, decode(new byte[]{2, 0, 1})); }
}
