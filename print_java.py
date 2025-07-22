import javaobj
import json

data = b"\xac\xed\x00\x05sr\x00\x13java.util.ArrayListx\x81\xd2\x1d\x99\xc7a\x9d\x03\x00\x01I\x00\x04sizexp\x00\x00\x00\x01w\x04\x00\x00\x00\x01sr\x00'me.chanjar.weixin.mp.bean.tag.WxUserTag\x94\xd4l\x047{\xc3,\x02\x00\x03L\x00\x05countt\x00\x13Ljava/lang/Integer;L\x00\x02idt\x00\x10Ljava/lang/Long;L\x00\x04namet\x00\x12Ljava/lang/String;xpsr\x00\x11java.lang.Integer\x12\xe2\xa0\xa4\xf7\x81\x878\x02\x00\x01I\x00\x05valuexr\x00\x10java.lang.Number\x86\xac\x95\x1d\x0b\x94\xe0\x8b\x02\x00\x00xp\x00\x00\x00\x00sr\x00\x0ejava.lang.Long;\x8b\xe4\x90\xcc\x8f#\xdf\x02\x00\x01J\x00\x05valuexq\x00~\x00\x08\x00\x00\x00\x00\x00\x00\x00\x02t\x00\t\xe6\x98\x9f\xe6\xa0\x87\xe7\xbb\x84x"  # 你的完整数据

objects = javaobj.loads(data)

for obj in objects:
    print("类名:", obj.classdesc.name)
    if hasattr(obj, 'attributes'):
        for k, v in obj.attributes.items():
            print(f"  {k}: {v}")

def java_obj_to_dict(obj):
    if hasattr(obj, 'attributes'):
        return {k: java_obj_to_dict(v) for k, v in obj.attributes.items()}
    elif isinstance(obj, list):
        return [java_obj_to_dict(i) for i in obj]
    else:
        return obj

print("\n转换为 JSON：")
print(json.dumps([java_obj_to_dict(o) for o in objects], ensure_ascii=False, indent=2))
