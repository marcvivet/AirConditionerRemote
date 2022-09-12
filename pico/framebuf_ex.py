import framebuf


class FrameBufferEx(framebuf.FrameBuffer):
    def __init__(self, *args, **kwargs) -> None:
        """
        Construct a FrameBuffer object.  The parameters are:

            - *buffer* is an object with a buffer protocol which must be large
              enough to contain every pixel defined by the width, height and
              format of the FrameBuffer.
            - *width* is the width of the FrameBuffer in pixels
            - *height* is the height of the FrameBuffer in pixels
            - *format* specifies the type of pixel used in the FrameBuffer;
              permissible values are listed under Constants below. These set the
              number of bits used to encode a color value and the layout of these
              bits in *buffer*.
              Where a color value c is passed to a method, c is a small integer
              with an encoding that is dependent on the format of the FrameBuffer.
            - *stride* is the number of pixels between each horizontal line
              of pixels in the FrameBuffer. This defaults to *width* but may
              need adjustments when implementing a FrameBuffer within another
              larger FrameBuffer or screen. The *buffer* size must accommodate
              an increased step size.

        One must specify valid *buffer*, *width*, *height*, *format* and
        optionally *stride*.  Invalid *buffer* size or dimensions may lead to
        unexpected errors.
        """
        self._buffer = args[0]
        self._width = args[1]
        self._height = args[2]
        super().__init__(*args, **kwargs)

    @property
    def buffer(self):
        return self._buffer

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
