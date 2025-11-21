#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import os
from datetime import datetime

MEDIA_EXT = {'.mp4', '.mkv', '.avi', '.flv', '.mov', '.wmv'}
TYPE_NAME = "Local_BF"



VOD_PIC_FOLDER = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfQAAAH0CAYAAADL1t+KAAAACXBIWXMAAAsTAAALEwEAmpwYAAASdUlEQVR4nO3d669ld13H8dVSWyyVFphLp8V2epnZu1UDCqgPNGijT1AkajAmGh4YJYAhUn2AGiNKNBpCSIhoBOucM0VKHRBtKd29MrRlpvPdncADEW8REpVwVQxGKAT6NYfSRBugnc535rvOWq938voLfiu/T/bZlzMMkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkjSf8s3D+bk5fG9uDi/JjeHXc2P4w9wc3pSbw0ZuDocYtdfloeFJ3c+QJOk0l68ZzsyN4dm5OVybG8O7c3P4eG4Oybb2dqMuSTMoczgjDw7Pz43hQG4Mnx7BAGHUJUmPt3zrsCc3h9fm5vDREQwORl2SdCLldcOluTm8MTeGz49gZDi9DuXh4azuZ1CSdBLlnw87c3N4S24OXxrBsNDHK3VJ2rbvkT/8CXXvj/MIr9QlaTuV1w2L3BiOjWBAGB+v1CVpO5Qbw0/n5vBfIxgOxssrdUkaa7kxPPlr75V3jwXbg1fqkjS2cmO4IDeHe0cwEmwvXqlL0ljKjeHC3Bw+OIJxYHsy6pLUXV4/XJYbw0dGMApsb/78LknN3y//hxGMAdPglbokne7yuuHbcnM4PoIRYFqMuiSdrrYu3Nwc7hrB5c80+fO7JJ2OcmP4/RFc+kybV+qSdCrLA8M1uTF8eQQXPtNn1CXplP3b043hkyO46JkPf36XpOpyY7hxBBc88+OVuiRVlQeGHx3Bxc58GXVJOtny0HC275szAkZdkk6mPDj86gguc9jiPXVJeiLlG4dzcnP42AgucniEV+qSdKLlweEVI7jA4dGMuiSd4C/CfXQElzd8Pf78LkmPpzwwvHAElzZ8M16pS9JjlRvDO0ZwYcNjMeqS9I3Ktw1Py83hwRFc1vB4GHVJ+nrl5vDSEVzScCK8py5Jjy43hneN4IKGE+WVuiQ9Ur5mODM3hs+M4HKGJ8KoS9JWeWD4nhFcynAyjLok5eZw7QguZDhZ3lOXNO9yYzgwgssYKnilLmm+5cZwdAQXMVQx6pLmmQ/EMUFGXdK8yrcNO0Zw+cKp4D11SfMpDw5XjeDihVPFK3VJ8ygPDM8bwaULp5JRlzT98sBwzQguXDjVjLqkaZcHhxeN4LKF08GoS5puuTG8uP2ivf7MzEPfmvk3F2SudmXe/czMe/dmvv+KzPv3ZR7bn7leAnAitu7Oo1d+JY9c8aW877L/yfdd8om8++LI2/cczNt3viLv37W7e4O03Qf94BmZ73hK5q07M++5NHO96H/wAeYmFpn37P1c3nXxfXn7rmvz8M7zujdJ22XQ335O5mpn5tF9/Q8yAP/f/fseyruf+eGvvnrP4czufdLYBv36MzJvuiDzvsv7H1YAHp8jlz+Yt++53qv2bdQpG/RHhvzolf0PJgBPzNZ78HdedGvevGdH916pY9D/+qmZRww5wGQcvfLLudr9hu7N0uka9BvOzjz87f0PHgCnxj17/zNXO36se7t0Kgf95qdlHvNpdYBZfDr+zj2HuvdL1YO+9R3yuy7uf8AAOL3ee8nH86bdl3XvmCoG/cZzMo9c0f9QAdDjyBVfytXOn+reMp3MoB86N/N+v+AGMHtH9z2Ut+1+Zfeezb4nNOh/dd7D76F0P0QAjMOxrffVd7++e9Nm3QkP+rue2v/gADBOK19t2x6D/o5zfZIdgPyGtv56u9r1m93bNsse96Df+GT/9QyAfEzH9j+Ut+76+e59m12Pa9D/4qyH/41p90MCwPb5ydhbdj67e+Nm1WMO+sEh8/Al/Q8HANvLvXs/m4eGs7t3bjY95qBv/c/y7ocCgO3pzove171zs+mbDvrWd81jBA8EANtTfPWT77/cvXXzHvSDZ2S+3/8wB2B5cu677MG8ec+53Xs330G/5Rn9DwEA03DXnlu6926eg37Dt/iKGgB1ju3PvGX393Vv3vwG/Y4L+w8fgGl57zP/rnvz5jXoW9859zvtAFSLReYdu76/e/fmM+i37e4/dACm6e6LP9C9e/MY9Lc+yatzAE7te+nv3rGve/umP+g3P63/sAGYtjv23Ni9fdMf9Hv29h80ANN2797/7t6+aQ/6DWf3HzIA83Drjhd07990B/09O/oPGIB5uPOi93bv33QH/X2X9h8wAPNw797Pdu/fNAf9+jN9uh2A0ycWmbfv3tW9gdMb9Hc+pf9wAZiX1e7f6N7A6Q26/3kOwOl250X3dG/g9Ab9rov7DxaAeTl8yb92b+D0Bv2+y/oPFoB5ef/lX+jewEmVbx1+xgfiADjtji0yDw9nde/gZMp3nvfy9kMFYJ5ufcbzundwMuVN5/9a+4ECME+37n5h9w5Oprz56b/VfqAAzNN7dv1i9w5Opnz3zt9rP1AA5um23a/u3sHJlKvdr28/UADm6bYLX9e9g5MpV7vf0H6gAMzTavcbundwMhl0ANqsDHpZBh2ANiuDXpZBB6DNyqCXZdABaLMy6GUZdADarAx6WQYdgDYrg16WQQegzcqgl2XQAWizMuhlGXQA2qwMelkGHYA2K4NelkEHoM3KoJdl0AFoszLoZRl0ANqsDHpZBh2ANiuDXpZBB6DNyqCXZdABaLMy6GUZdADarAx6WQYdgDYrg16WQQegzcqgl2XQAWizMuhlGXQA2qwMelkGHYA2K4NelkEHoM3KoJdl0AFoszLoZRl0ANqsDHpZBh2ANiuDXpZBB6DNyqCXZdABaLMy6GUZdADarAx6WQYdgDYrg16WQQegzcqgl2XQAWizMuhlGXQA2qwMelkGHYA2K4NelkEHoM3KoJdl0AFoszLoZRl0ANqsDHpZBh2ANiuDXpZBB6DNyqCXZdABaLMy6GXlPZe+rP1AAZiney59WfcOTqaMxYvbDxSAeYrFi7t3cDIZdADahEEvy6AD0CYMelkGHYA2YdDLMugAtAmDXpZBB6BNGPSyDDoAbcKgl2XQAWgTBr0sgw5AmzDoZRl0ANqEQS/LoAPQJgx6WQYdgDZh0Msy6AC0CYNelkEHoE0Y9LIMOgBtwqCXZdABaBMGvSyDDkCbMOhlGXQA2oRBL8ugA9AmDHpZBh2ANmHQyzLoALQJg16WQQegTRj0sgw6AG3CoJdl0AFoEwa9LIMOQJsw6GUZdADahEEvy6AD0CYMelkGHYA2YdDLMugAtAmDXpZBB6BNGPSyDDoAbcKgl2XQAWgTBr0sgw5AmzDoZRl0ANqEQS/LoAPQJgx6WQYdgDZh0Msy6AC0CYNelkEHoE0Y9LIMOgBtwqCXZdABaBMGvSyDDkCbMOhlGXQA2oRBL8ugA9AmDHpZBh2ANmHQyzLoALQJg16WQQegTRj0sgw6AG3CoJdl0AFoEwa9LIMOQJsw6GUZdADahEEvy6AD0CYMelkGHYA2YdDLMugAtDHodRl0ANqEQS/LoAPQJgx6WQYdgDZh0Msy6AC0CYNelkEHoE0Y9LIMOgBtwqCXZdABaBMGvSyDDkCbMOhlGXQA2oRBL8ugA9AmDHpZBh2ANmHQyzLoALQJg16WQQegTRj0sgw6AG3CoJdl0AFoEwa9LIMOQJsw6GUZdADahEEvy6AD0CYMelkGHYA2YdDLMugAtAmDXpZBB6BNGPSyDDoAbcKgl2XQAWgTBr0sgw5AmzDoZRl0ANqEQS/LoAPQJgx6WQYdgDZh0Msy6AC0CYNelkEHoE0Y9LIMOgBtwqCXZdABaBMGvSyDDkCbMOhlGXQA2oRBL8ugA9AmDHpZBh2ANmHQyzLoALQJg16WQQegTRj0sgw6AG3CoJdl0AFoEwa9LIMOQJsw6GUZdADahEEvy6AD0CYMelkGHYA2YdDLMugAtAmDXpZBB6BNGPSyDDoAbcKgl2XQAWgTBr0sgw5AmzDoZRl0ANqEQS/LoAPQJgx6WQYdgDZh0Msy6AC0CYNelkEHoE0Y9LIMOgBtwqCXZdABaBMGvSyDDkCbMOhlGXQA2oRBL8ugA9AmDHpZBh2ANmHQyzLoALQJg16WQQegTRj0sgw6AG3CoJdl0AFoEwa9LIMOQJsw6GUZdADahEEvy6AD0CYMelkGHYA2YdDLMugAtAmDXpZBB6BNGPSyDDoAbcKgl2XQAWgTBr0sgw5AmzDoZRl0ANqEQS/LoAPQJgx6WQYdgDZh0Msy6AC0CYNelkEHoE0Y9LIMOgBtwqCXZdABaBMGvSyDDkCbMOhlGXQA2oRBL8ugA9AmDHpZBh2ANmHQyzLoALQJg16WQQegTRj0sgw6AG3CoJdl0AFoEwa9LIMOQJsw6GUZdADahEEvy6AD0CYMelkGHYA2YdDLMugAtAmDXpZBB6BNGPSyDDoAbcKgl2XQAWgTBr0sgw5AmzDoZRl0ANqEQS/LoAPQJgx6WQYdgDZh0Msy6AC0CYNelkEHoE0Y9LIMOgBtwqCXZdABaBMGvSyDDkCbMOhlGXQA2oRBL8ugA9AmDHpZBh2ANmHQyzLoALQJg16WQQegTRj0sgw6AG3CoJdl0AFoEwa9LIMOQJsw6GUZdADahEEvKx/Y/6L2AwVgphY/0b2DkymP7b+m/0ABmKUHFj/UvYOTKdf7n9d+oADM07Hlc7p3cDLl/fuuaj9QAOYplvu7d3Ay5fH9O9oPFIB5Onr107t3cFLlevGZ9kMFYF5i+anu/ZtcGcsj7QcLwLzE8r7u/ZtcGcsD7QcLwMwsruvev8mVDyyv7T9YAGbmVd37N7lyfdV3j+BgAZiTY/ue1b1/kytzODNj+en2wwVgJhaf2dqe7v2bZBnLd/YfMAAz8ZfduzfZMpa/NIIDBmAWFr/QvXuTLY9ffn6ul5/vP2QAJu4L+cFnXdC9e5Mu18tDIzhoAKYsFm/v3rvJl7H88faDBmDaHrjqBd17N/ny8PPPyvXyI+2HDcBUfWRra7r3bhZl7H/5CA4cgGl6affOzab8pyvPyfXy30dw6ABMy79tbUz3zs2qrZ/jG8HBAzAlsXhl977NrvzQ1Wfnevnh9sMHYCIW/+jVeVO5Xj4/Y/lQ/0MAwLZ3bP813bs26zIWN7Q/BABsb7G4vnvPZl/G1RfmevGJ9ocBgG1q8fE8cvmu7j3T1qgfW/xwrpdf7n8oANhWYvmVXF/1I907pv9TrhevbX8wANhufrt7v/So8tDwpFwvbh/BwwHAdhDLW/2/85GWx59zbq4XR9sfEgDGLZbr/NDV53Xvlr5JeXz/jozl37c/LACMUyz+2Yfgtkl5/2Kvf+ACQD5aLP9layO6d0on+nW2WHyg/eEBYBxi8bd5dN/F3fukJ9DW+yMZizvaHyIAesXycB6//PzuXdJJlIcvfXKul3/S/jAB0CMWb/Ib7RMqY/mTGYvPtj9YAJwun8v18me790enoLz/qn0ZyyMjeMgAOJVieV8ev/KK7t3RKSxzOCOPLV+SsfxU+wMHQLHFf+R68St+MGZGZSyfkbH804zFF/sfQABOSiy+mLH44zx69dO790VN5fGrL8n18o25Xn6+/YEE4MTE8sGM5Ztz/R3f3r0nGtf31n/XD9IAbJMfiInF72zd3d37oVG/x37VD+Z68We5Xn6y/aEF4GsWn8j14i15fP8PbN3V3Xuh7TbuxxfflevlqzKWN2csP9b/QAPMxNadG8ubvvoht/XyO424SstjVz41Y/HcjMXPZSxfnevFH2Qs/ijXy41cLw8BcEI2Hr5Dt+7S5asfvlsXz926a7vve0mSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEkaTl//C3kbhPhagkd6AAAAAElFTkSuQmCC"



VOD_PIC_VIDEO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEkElEQVR4nO2W609TdxzG+RsExDfAXi0wKdsy57KBDDiKU5juwm2bcXPOzRjZwCnlquUi2ViC3O+3lrZAW0qiZO7tXs0sgyn6ytDidAicntOrr6DJs/xOT1vS2vb0EuiSPsknTU+b/J7n2+f3TePiYooppphiiolX2hxdmK7d/Dd9nkY0kja/+SxdS5+I8yXuC1FgNN1fCO3mU58B9tpcegAOztPI1NL43wUQaWm8MWfAIY0B72gMwgIssVtwapHZ2nXTSzvO/9uwhXfVDI6oGOSqGGEBPLXbVfFU/iyDYzMMPphmozuASEvjrTmD1/knpll8qGTxkUJgAFIbp/7apQplammu5++pGSwbtl3nP6K38bGCRYnciPIpY3Re4te1BrytMSBbzXB1OT7DooifODH+2ZQRZ2RGfCWNwgCZTvMqh3nS81NKFp/KWZTtMP7NpAnfTZiiK4BIS7vMU7MM1/XTShbFcpab+pdSI85PGnFxwoTL4yZ8P2aKnjV6kL+wWWr35Il5UpnHtPsOrGxsc8avjJpxbdQc2S2UptnAqxOPuddgA7w5Z+D2ex7pPF8bYv4LmdHr/KujZtSMmFE/HMEAqa2/I76wHfuOtyG+qJ17L7z3NA5rDMhRMSiYcaxIUpvPZUack3oHqBsx4/qwBc1Dlsis0eS637Cv4KYXyeKFgOZfm3dXh5plcHKaxScKR+fJZf12wgTdhrtCq+vbkAxZ0DpowU+DAgP4I6XuLuKPtfokWXwn4NYh/2lyVY7qnFawKJUbcVZmxIVJx2WtGjNDPGJGw7AZTUMW3By0oH3Aio5+a3gBHOZbAuIvxCG1ATnSdRxVMijk1yXp/deTRlwaN6FyzITqUUffifm2QQt+GbDiVr8V3X1hBEipvYv4oy2CSa72DnG4R4/8yiVQFYugfljCyY5VbteTdUl2PNk25MKSzkv4yRPznf1W9PRZMdBrDW2NptT+igSqOWhSqm+7zXesOIx7cKpthdv1ZPpVYyauOk837K7z157bXeZHegQG8FQC1RQyJIQv8xRPcavONf36EbPX+U7zE922EAPkS0Imo3zar3mKp7xFx02frEtPDfdYMd5tg6zLFvwa/WP5CRLyboRERplSkHmK50yzjuv+s3V3hZ6v2THWbYO0ywZlp8AAqTULSMy7HhbBmqd4zjXp8DN/cft6rdz0SXXknTbM3BIQIFW8gMTcxrDIKFOEZJ7iuSDRo4u/uKM7pq/qCBAgVXwHibkNYRGueYrnokSPwV4rVx/SfTJ9tb8AnPn36zn+fPiPq4P3lp+4ngcio1QeEfOP9C9c52+s2THF10fT8cJ3gP05dXDiqZ2f+UIUIfNUxaLX+STAbOAAtXDiHaDWL6LSqYiZp14SoLJRL+AXOFIDJ/cerLrX6INV1/OXISqJrHmqYhEPdTbX+csrNu7ZlUa9/zuwP1uMYBGVyCJunvLDjw163wGSsqsRDLttnuLxGeBAgcSelHUNQhAVS/fEfFHVfbvPAK9cVjQeKLhhT8q6Cn/slfnCqvv2S/X6Bp8BYooppphiigtS/wHAKG/m+NkZXQAAAABJRU5ErkJggg=="



SUB_EXT = {"srt", "ass", "ssa", "sub", "idx", "vtt"}

class Spider(Spider):
    def getName(self):
        return "本地文件"

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        return url.lower().endswith(tuple(MEDIA_EXT))

    def manualVideoCheck(self):
        return False

    def homeContent(self, filter):
        classes = [{"type_id": "/sdcard", "type_name": "📁本地视频", "type_flag": "1", "type_vod": "1"}]
        result = {"class": classes, "list": []}
        return result

    def categoryContent(self, tid, pg, filter, extend):
        result = {"list": [], "page": int(pg), "pagecount": 1, "limit": 0, "total": 0}
        if not os.path.exists(tid) or not os.access(tid, os.R_OK):
            return result

        items = []
        for item in os.listdir(tid):
            item_path = os.path.join(tid, item)
            if item.startswith("."):
                continue
            if os.path.isdir(item_path):
                vod = {
                    "id": item_path,
                    "vod_id": item_path,
                    "vod_name": item,
                    "vod_pic": VOD_PIC_FOLDER,
                    "vod_remarks": datetime.fromtimestamp(os.path.getmtime(item_path)).strftime("%Y/%m/%d %H:%M:%S"),
                    "vod_tag": "folder",
                    "type_name": TYPE_NAME
                }
                items.append(vod)
            elif os.path.splitext(item)[1].lower() in MEDIA_EXT:
                file_size = self.format_size(os.path.getsize(item_path))
                full_url = f"file://{item_path}"
                vod = {
                    "id": item_path,
                    "vod_id": item_path,
                    "vod_name": item,
                    "vod_pic": VOD_PIC_VIDEO,
                    "vod_remarks": f"{file_size} | {datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%Y/%m/%d')}",
                    "vod_tag": "video",
                    "type_name": TYPE_NAME,
                    "is_video": "1",
                    "vod_type": "1",
                    "isVod": "1",
                    "vod_play_from": "播放",
                    "vod_play_url": f"1${full_url}"
                }
                items.append(vod)

        result["list"] = items
        result["limit"] = len(items)
        result["total"] = len(items)
        return result

    def detailContent(self, array):
        result = {"list": []}
        if not array:
            return result

        if isinstance(array, str):
            vod_id = array
        elif isinstance(array, list) and len(array) > 0:
            vod_id = array[0]
        else:
            return result

        vod_id = os.path.abspath(vod_id)
        if os.path.isfile(vod_id) and os.path.splitext(vod_id)[1].lower() in MEDIA_EXT:
            full_url = f"file://{vod_id}"
            vod = {
                "id": vod_id,
                "vod_id": vod_id,
                "vod_name": os.path.basename(vod_id),
                "type_name": TYPE_NAME,
                "vod_type": "1",
                "vod_play_from": "播放",
                "vod_play_url": f"1${full_url}",
                "vod_pic": VOD_PIC_VIDEO,
                "vod_remarks": "强制播放本地文件"
            }
            result["list"].append(vod)

        return result

    def playerContent(self, flag, id, vipFlags):
        if not id.startswith("file://"):
            id = f"file://{os.path.abspath(id)}"
        result = {"url": id, "parse": 0}
        return result

    def localProxy(self, param):
        return [200, "application/octet-stream", None, ""]

    def format_size(self, size):
        units = ["B", "KB", "MB", "GB"]
        unit_idx = 0
        while size >= 1024 and unit_idx < len(units)-1:
            size /= 1024
            unit_idx += 1
        return f"{size:.1f}{units[unit_idx]}"

if __name__ == "__main__":
    spider = Spider()
    spider.init()