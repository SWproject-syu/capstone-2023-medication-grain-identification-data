export type ResponseType = {
  header: {
    resultCode: string; //'00'
    resultMsg: string; //'NORMAL SERVICE.'
  };
  body: {
    pageNo: number; //1;
    totalCount: number; //24881;
    numOfRows: number; //300;
    items: ItemType[];
  };
};

export type ItemType = {
  ITEM_SEQ: string; // "200808876"; 	품목일련번호; 200402488
  ITEM_NAME: string; // "가스디알정50밀리그램(디메크로틴산마그네슘)"; 품목명; 알레기살정10밀리그람(페미로라스트칼륨)
  ENTP_SEQ: string; // "19540006"; 업체일련번호; 	19660001
  ENTP_NAME: string; // "일동제약(주)"; 	업체명; 	현대약품(주)
  CHART: string; // "녹색의 원형 필름코팅정"; 성상; 띠 모양 할선이 있는 황백색 원형정제이다
  ITEM_IMAGE: string; // 큰제품이미지; "https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/147426403087300104";
  PRINT_FRONT: string; // "IDG"; 표시(앞); 마크226
  PRINT_BACK: string | null; // null; 	표시(뒤); 	분할선
  DRUG_SHAPE: string; // "원형"; 	의약품모양;
  COLOR_CLASS1: string; // "연두"; 	색깔(앞);
  COLOR_CLASS2: string | null; // null; 	색깔(뒤);
  LINE_FRONT: string | null; // null; 	분할선(앞);
  LINE_BACK: string | null; // null; 분할선(뒤);
  LENG_LONG: string; // "7.6"; 	크기(장축);
  LENG_SHORT: string; // "7.6"; 	크기(단축);
  THICK: string; // "3.6"; 크기(두께);
  IMG_REGIST_TS: string; // "20100326"; 약학정보원 이미지 생성일;
  CLASS_NO: string; // "02390"; 분류번호;
  CLASS_NAME: string; // "기타의 소화기관용약"; 분류명 기타의 알레르기용약;
  ETC_OTC_NAME: string; // "전문의약품"; 전문/일반;
  ITEM_PERMIT_DATE: string; // "20080820"; 품목허가일자; 20040325
  FORM_CODE_NAME: string; // "당의정"; 제형코드이름; 나정
  MARK_CODE_FRONT_ANAL: string; // ""; 마크내용(앞); ↔,+
  MARK_CODE_BACK_ANAL: string; // "";	마크내용(뒤);
  MARK_CODE_FRONT_IMG: string; // ""; 마크이미지(앞); https://nedrug.mfds.go.kr/pbp/cmn/itemImageDownload/147938644048800199
  MARK_CODE_BACK_IMG: string; // ""; 마크이미지(뒤);
  ITEM_ENG_NAME: string | null; // null; 제품영문명; Alegysal Tab. 10mg
  CHANGE_DATE: string; // "20130129"; 변경일자;
  MARK_CODE_FRONT: string | null; // null; 마크코드(앞);
  MARK_CODE_BACK: string | null; // null; 마크코드(뒤);
  EDI_CODE: string | null; // null; 보험코드; 642003260;
};
