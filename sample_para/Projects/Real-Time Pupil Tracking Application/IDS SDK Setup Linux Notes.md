# IDS SDK Setup & Linux Configuration Notes

**Project:** Real-Time Pupil Tracking Application  
**OS:** Ubuntu 22.04 LTS  
**SDK Version:** IDS uEye 4.96.1  
**Last Updated:** 2025-01

---

## Installation Procedure

### Step 1: Download SDK
```bash
# From IDS Vision website (requires account)
wget https://en.ids-imaging.com/downloads/... # (link from IDS portal)
chmod +x uEye_4.96.1_64bit.run
sudo ./uEye_4.96.1_64bit.run
```

### Step 2: Install Dependencies
```bash
sudo apt install libqt5widgets5 libusb-1.0-0 libqt5network5
```

### Step 3: Start uEye Service
```bash
sudo systemctl start ueyeusbdrc
sudo systemctl enable ueyeusbdrc  # Start on boot
```

### Step 4: Verify Camera Detection
```bash
/usr/bin/ueyesetid  # Check camera ID assignment
ls /dev/video*      # Should show /dev/video0 or similar
```

---

## Python Wrapper: pyueye

IDS provides an official Python binding:
```bash
pip install pyueye
```

**Critical note:** pyueye wraps the C SDK via ctypes. Many parameters use ctypes data types, not native Python types. Always check return codes:
```python
from pyueye import ueye

def check(ret):
    if ret != ueye.IS_SUCCESS:
        raise Exception(f"uEye error: {ret}")

check(ueye.is_InitCamera(hCam, None))
```

---

## Camera Configuration (Tuned Settings)

```python
# Exposure: NIR illumination requires short exposure to freeze motion
ueye.is_Exposure(hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE, 
                 ueye.c_double(5.0), 8)  # 5ms exposure

# Gain: Keep gain low to reduce noise
ueye.is_SetHardwareGain(hCam, 30, ueye.IS_IGNORE_PARAMETER,
                         ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER)

# Gamma: Set to 1.0 (linear response, better for segmentation)
ueye.is_Gamma(hCam, ueye.IS_GAMMA_CMD_SET, ueye.c_int(100), 4)  # 1.00 gamma

# Color mode: 8-bit monochrome
ueye.is_SetColorMode(hCam, ueye.IS_CM_MONO8)
```

---

## Frame Acquisition Loop

```python
import numpy as np
import cv2

def get_frame(hCam, mem_ptr, width, height):
    array = ueye.get_data(mem_ptr, width, height, 8, width, copy=True)
    frame = np.reshape(array, (height, width))
    return frame

# Main loop
while True:
    ret = ueye.is_WaitForNextImage(hCam, 1000, mem_ptr, mem_id)
    if ret == ueye.IS_SUCCESS:
        frame = get_frame(hCam, mem_ptr, 1280, 1024)
        # Process frame...
        ueye.is_UnlockSeqBuf(hCam, mem_id, mem_ptr)
    
    if cv2.waitKey(1) == ord('q'):
        break
```

---

## Troubleshooting Log

| Problem | Cause | Solution |
|---------|-------|---------|
| `IS_NO_SUCCESS` on init | uEye service not running | `sudo systemctl start ueyeusbdrc` |
| Camera not detected | USB permission | Add user to `video` group: `sudo usermod -aG video $USER` |
| Green tint in image | Wrong color mode | Set `IS_CM_MONO8` explicitly |
| Frame drop at 60fps | USB bandwidth | Reduce to 1280×512 ROI or use GigE camera |
| Segfault in pyueye | ctypes mismatch | Ensure pyueye version matches SDK version |

---

## USB vs. GigE Considerations

Our current setup uses USB3 (UI-3060CP). For future lab deployment:
- GigE cameras offer more deterministic frame delivery
- USB3 is sufficient for research at 60fps with proper buffering
- Driver-level timestamping available via `ueye.UEYETIME` struct

---

## Resources
- IDS Software Suite documentation: `/usr/share/doc/ueyesdk/`
- Python examples: `/usr/share/doc/ueyesdk/examples/python/`
- Forum: https://en.ids-imaging.com/ids-forum

