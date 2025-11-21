import sys
sys.path.append('..')  # 参考模板：调整路径，适配TVBox环境
from base.spider import Spider  # 继承与参考模板一致的基础Spider
import json
import requests
import urllib.parse

class Spider(Spider):
    # 核心配置：与参考模板结构一致
    header = {
        "Host": "frodo.douban.com",
        "Connection": "Keep-Alive",
        "Referer": "https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; MI 9 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3163 MMWEBSDK/20230701 Mobile Safari/537.36 MMWEBID/6553 MicroMessenger/8.0.40.24200(0x2800285A) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
    }
    site_url = "https://frodo.douban.com/api/v2"
    apikey = "?apikey=0ac44ae016490db2204ce0a042db2916"

    def getName(self):
        return "🎉 缤纷影视"  # 与你的接口配置name一致

    def init(self, extend=""):
        # 参考模板：简化初始化，仅打印日志（无单例、无复杂逻辑）
        print("豆瓣爬虫初始化，扩展参数：", extend)
        self.extend = extend

    def isVideoFormat(self, url):
        # 参考模板：空实现（必须保留，避免报错）
        pass

    def manualVideoCheck(self):
        # 参考模板：空实现（必须保留，避免报错）
        pass

    def homeContent(self, filter):
        # 完全参考模板结构：直接返回字典，不转JSON字符串
        result = {}
        # 1. 分类列表（严格匹配 type_id + type_name）
        type_ids = ["hot_gaia", "tv_hot", "show_hot", "movie", "tv", "rank_list_movie", "rank_list_tv"]
        type_names = ["热门电影", "热播剧集", "热播综艺", "电影筛选", "电视筛选", "电影榜单", "电视剧榜单"]
        classes = []
        for tid, tname in zip(type_ids, type_names):
            classes.append({
                "type_id": tid,
                "type_name": tname
            })
        result["class"] = classes

        # 2. 推荐视频列表（参考模板，先简化获取逻辑）
        recommend_url = f"{self.site_url}/subject_collection/subject_real_time_hotest/items{self.apikey}"
        try:
            # 参考模板的请求方式：简洁，无多余参数
            rsp = requests.get(recommend_url, headers=self.header, timeout=10)
            rsp.encoding = rsp.apparent_encoding or 'utf-8'
            data = json.loads(rsp.text)
            items = data.get("subject_collection_items", [])
            vods = []
            for item in items:
                vods.append({
                    "vod_id": f"msearch:{item.get('id', '')}",
                    "vod_name": item.get("title", "未知名称"),
                    "vod_pic": self.getPic(item),
                    "vod_remarks": self.getRating(item)  # 字段名正确，与参考模板一致
                })
            result["list"] = vods
        except Exception as e:
            print("推荐内容获取失败：", str(e))
            result["list"] = []

        # 3. 筛选配置（参考模板，简化为固定格式）
        if filter:
            result["filters"] = self.config["filter"]
        return result

    def homeVideoContent(self):
        # 参考模板：返回空列表
        result = {"list": []}
        return result

    def categoryContent(self, tid, pg, filter, extend):
        # 参考模板结构：直接返回字典，分页字段用整数
        result = {}
        extend = extend or {}
        sort = extend.get("sort", "T")
        tags = urllib.parse.quote(self.getTags(extend))
        start = (int(pg) - 1) * 20
        cate_url = ""
        item_key = "items"

        # 分类URL逻辑不变，简化请求
        if tid == "hot_gaia":
            sort = extend.get("sort", "recommend")
            area = urllib.parse.quote(extend.get("area", "全部"))
            sort = f"{sort}&area={area}"
            cate_url = f"{self.site_url}/movie/hot_gaia{self.apikey}&sort={sort}&start={start}&count=20"
        elif tid == "tv_hot":
            type_val = extend.get("type", "tv_hot")
            cate_url = f"{self.site_url}/subject_collection/{type_val}/items{self.apikey}&start={start}&count=20"
            item_key = "subject_collection_items"
        elif tid == "show_hot":
            show_type = extend.get("type", "show_hot")
            cate_url = f"{self.site_url}/subject_collection/{show_type}/items{self.apikey}&start={start}&count=20"
            item_key = "subject_collection_items"
        elif tid == "tv":
            cate_url = f"{self.site_url}/tv/recommend{self.apikey}&sort={sort}&tags={tags}&start={start}&count=20"
        elif tid == "rank_list_movie":
            rank_type = extend.get("榜单", "movie_real_time_hotest")
            cate_url = f"{self.site_url}/subject_collection/{rank_type}/items{self.apikey}&start={start}&count=20"
            item_key = "subject_collection_items"
        elif tid == "rank_list_tv":
            rank_type = extend.get("榜单", "tv_real_time_hotest")
            cate_url = f"{self.site_url}/subject_collection/{rank_type}/items{self.apikey}&start={start}&count=20"
            item_key = "subject_collection_items"
        else:
            cate_url = f"{self.site_url}/movie/recommend{self.apikey}&sort={sort}&tags={tags}&start={start}&count=20"

        # 参考模板的请求方式
        try:
            print("请求分类URL：", cate_url)
            rsp = requests.get(cate_url, headers=self.header, timeout=10)
            rsp.encoding = rsp.apparent_encoding or 'utf-8'
            data = json.loads(rsp.text)
            items = data.get(item_key, [])
            vods = []
            for item in items:
                vods.append({
                    "vod_id": f"msearch:{item.get('id', '')}",
                    "vod_name": item.get("title", "未知名称"),
                    "vod_pic": self.getPic(item),
                    "vod_remarks": self.getRating(item)
                })
            result["list"] = vods
        except Exception as e:
            print("分类内容获取失败：", str(e))
            result["list"] = []

        # 分页字段用整数（与参考模板一致，之前改为字符串是错误的！）
        result["page"] = int(pg)
        result["pagecount"] = 9999
        result["limit"] = 20
        result["total"] = 999999
        return result

    def detailContent(self, array):
        # 参考模板：array是列表，取第一个元素
        ids = array[0] if array else ""
        douban_id = ids.split(":")[-1] if ":" in str(ids) else str(ids)
        result = {"list": []}
        if not douban_id:
            print("视频ID获取失败")
            return result

        detail_url = f"{self.site_url}/movie/{douban_id}{self.apikey}"
        try:
            rsp = requests.get(detail_url, headers=self.header, timeout=10)
            rsp.encoding = rsp.apparent_encoding or 'utf-8'
            data = json.loads(rsp.text)
            # 完全参考模板的字段格式
            vod = {
                "vod_id": ids,
                "vod_name": data.get("title", "未知名称"),
                "vod_pic": self.getPic(data),
                "type_name": ",".join(data.get("genres", [])),
                "vod_year": data.get("year", ""),
                "vod_area": "",
                "vod_remarks": self.getRating(data),
                "vod_actor": ",".join([a.get("name", "") for a in data.get("casts", [])]),
                "vod_director": ",".join([d.get("name", "") for d in data.get("directors", [])]),
                "vod_content": data.get("intro", "").strip() or data.get("summary", "").strip(),
                "vod_play_from": "豆瓣播放源",
                "vod_play_url": f"播放链接$https://xxx.com/play?douban_id={douban_id}"  # 占位符
            }
            result["list"] = [vod]
        except Exception as e:
            print("详情获取失败：", str(e))
        return result

    def searchContent(self, key, quick):
        # 参考模板：空实现，返回空列表
        result = {"list": []}
        return result

    def playerContent(self, flag, id, vipFlags):
        # 参考模板：实现播放链接解析（简单返回占位符）
        result = {}
        result["parse"] = 0
        result["playUrl"] = ""
        result["url"] = id  # 直接返回传入的播放链接
        result["header"] = self.header
        return result

    def localProxy(self, param):
        # 参考模板：空实现
        return [200, "video/MP2T", None, ""]

    # 辅助方法（简化，无多余逻辑）
    def getRating(self, item):
        try:
            rating = item.get("rating", {})
            score = rating.get("value", "")
            return f"评分：{score}" if score else ""
        except:
            return ""

    def getPic(self, item):
        try:
            pic = item.get("pic", {})
            normal_pic = pic.get("normal", "")
            if not normal_pic:
                return ""
            # 参考模板：不拼接Referer/UA，先简化（避免特殊字符问题）
            return normal_pic
        except:
            return ""

    def getTags(self, extend):
        try:
            tags = []
            for key, value in extend.items():
                if key != "sort" and value and str(value).strip():
                    tags.append(str(value).strip())
            return ",".join(tags)
        except:
            return ""

    # 筛选配置（参考模板格式）
    config = {
        "filter": {
            "movie": [
                {"key": "genre", "name": "类型", "value": [{"n": "喜剧", "v": "喜剧"}, {"n": "动作", "v": "动作"}, {"n": "科幻", "v": "科幻"}]},
                {"key": "area", "name": "地区", "value": [{"n": "大陆", "v": "大陆"}, {"n": "美国", "v": "美国"}, {"n": "韩国", "v": "韩国"}]}
            ],
            "tv": [
                {"key": "genre", "name": "类型", "value": [{"n": "古装", "v": "古装"}, {"n": "现代", "v": "现代"}, {"n": "悬疑", "v": "悬疑"}]}
            ]
        }
    }

# 测试入口（本地运行验证）
if __name__ == "__main__":
    douban = Spider()
    douban.init()
    home = douban.homeContent(filter=False)
    print("首页内容：", home)