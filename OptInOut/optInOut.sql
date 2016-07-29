-- Table: acc.opt_in_out

-- DROP TABLE acc.opt_in_out;

CREATE TABLE acc.opt_in_out
(
  opt_in_out_id bigint NOT NULL DEFAULT nextval('opt_in_out_opt_id_seq'::regclass), -- Uniquely identifies a customers phone preference
  customer_nbr character varying(20), -- Customer number
  phone_nbr character varying(17), -- Customer phone
  opt_in_sw boolean DEFAULT false,
  opt_type character varying(11) DEFAULT 'SMSOTHER'::character varying,
  source_bus_unit bigint, -- Associated Group that preference came from
  created_dt timestamp without time zone DEFAULT now(), -- date preference was entered
  last_modified_dt timestamp without time zone DEFAULT now(),
  audit_comment text,
  CONSTRAINT opt_in_out_pkey PRIMARY KEY (opt_in_out_id),
  CONSTRAINT customer_belongs_to FOREIGN KEY (source_bus_unit)
      REFERENCES shr.bo_bus_unit (bus_unit_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE acc.opt_in_out
  OWNER TO adp_dba;
GRANT ALL ON TABLE acc.opt_in_out TO adp_dba;
GRANT ALL ON TABLE acc.opt_in_out TO adp_apps_grp;
GRANT SELECT ON TABLE acc.opt_in_out TO adp_support_grp;
COMMENT ON COLUMN acc.opt_in_out.opt_in_out_id IS 'Uniquely identifies a customers phone preference';
COMMENT ON COLUMN acc.opt_in_out.customer_nbr IS 'Customer number';
COMMENT ON COLUMN acc.opt_in_out.phone_nbr IS 'Customer phone';
COMMENT ON COLUMN acc.opt_in_out.source_bus_unit IS 'Associated Group that preference came from';
COMMENT ON COLUMN acc.opt_in_out.created_dt IS 'date preference was entered';

-- View: acc.opt_in_out_mg_v

-- DROP VIEW acc.opt_in_out_mg_v;

CREATE OR REPLACE VIEW acc.opt_in_out_mg_v AS 
 SELECT oio.opt_in_out_id, oio.customer_nbr, oio.phone_nbr, oio.opt_in_sw, oio.opt_type, oio.source_bus_unit, oio.created_dt, oio.last_modified_dt, oio.audit_comment, bo.bus_unit_id
   FROM opt_in_out oio
   JOIN bo_bus_unit bo ON bo.bus_unit_id = oio.source_bus_unit;

ALTER TABLE acc.opt_in_out_mg_v
  OWNER TO adp_dba;
GRANT ALL ON TABLE acc.opt_in_out_mg_v TO adp_dba;
GRANT ALL ON TABLE acc.opt_in_out_mg_v TO adp_apps_grp;
GRANT SELECT ON TABLE acc.opt_in_out_mg_v TO adp_support_grp;

-- View: acc.opt_in_out_v

-- DROP VIEW acc.opt_in_out_v;

CREATE OR REPLACE VIEW acc.opt_in_out_v AS 
 SELECT oio.opt_in_out_id, oio.customer_nbr, oio.phone_nbr, oio.opt_in_sw, oio.opt_type, oio.source_bus_unit, oio.created_dt, oio.last_modified_dt, oio.audit_comment, bo.bus_unit_id, bo.bus_unit_cd
   FROM opt_in_out oio
   JOIN bo_bus_unit bo ON bo.bus_unit_id = oio.source_bus_unit;

ALTER TABLE acc.opt_in_out_v
  OWNER TO adp_dba;
GRANT ALL ON TABLE acc.opt_in_out_v TO adp_dba;
GRANT ALL ON TABLE acc.opt_in_out_v TO adp_apps_grp;
GRANT SELECT ON TABLE acc.opt_in_out_v TO adp_support_grp;

-- Function: acc.opt_in_out_ins_updt(character varying, character varying, character varying, boolean, text, character varying)

-- DROP FUNCTION acc.opt_in_out_ins_updt(character varying, character varying, character varying, boolean, text, character varying);

CREATE OR REPLACE FUNCTION acc.opt_in_out_ins_updt(character varying, character varying, character varying, boolean, text, character varying)
  RETURNS crud_fcn_return_rs AS
$BODY$

DECLARE
  _busUnit ALIAS FOR $1;
  _customer_nbr ALIAS FOR $2;
  _phone_nbr ALIAS FOR $3;
  _opt_in_sw ALIAS FOR $4;
  _text ALIAS FOR $5;
  _opt_type ALIAS FOR $6;
--
  intRowCount int;
  dtLastModDate varchar;
  strFunctionName varchar;
  intOptId int8;
  rsReturn crud_fcn_return_rs;
  busUnitId bigint;

BEGIN
  strFunctionName := 'opt_in_out_ins_updt';
  dtLastModDate :=  (('now'::text)::timestamp(6) without time zone)::text;

  SELECT INTO busUnitId bus_unit_id FROM shr.bo_bus_unit WHERE bus_unit_cd = _busUnit;

  IF busUnitId IS NOT NULL THEN
    
  SELECT INTO IntOptId opt_in_out_id FROM opt_in_out WHERE customer_nbr = _customer_nbr AND phone_nbr = _phone_nbr AND source_bus_unit = busUnitId AND opt_type = _opt_type;
  
  IF intOptId IS NULL THEN
    INSERT INTO opt_in_out (source_bus_unit, customer_nbr, phone_nbr, opt_in_sw, audit_comment, opt_type)
    VALUES (busUnitId,_customer_nbr,_phone_nbr,_opt_in_sw,_text,_opt_type);

    GET DIAGNOSTICS  intRowCount = ROW_COUNT;

    IF intRowCount <> 1 THEN
      RAISE NOTICE 'Error# -1: Function % failed to insert phone_nbr %, bus_unit % into table opt_in_out', 
      strFunctionName,_phone_nbr, busUnitId;
      rsReturn.status_nbr := -1;
      rsReturn.return_txt = 'Error: failed to insert', intOptId;
      RETURN rsReturn;
    END IF;
  END IF;
  
  UPDATE opt_in_out 
     SET opt_in_sw = _opt_in_sw,
        last_modified_dt = (dtLastModDate::timestamp(6) without time zone),
      audit_comment = _text
   WHERE phone_nbr = _phone_nbr 
     AND source_bus_unit = busUnitId
     AND opt_type = _opt_type;

  GET DIAGNOSTICS  intRowCount = ROW_COUNT;

  IF intRowCount >= 1 THEN
     rsReturn.row_id := intOptId;
     rsReturn.last_modified_dt := (dtLastModDate::timestamp(6) without time zone);
     rsReturn.status_nbr := 0; 
     RETURN rsReturn;
  ELSE
     RAISE NOTICE 'Error# -1: Function % failed to update phone_nbr %, bus_unit %', 
       strFunctionName, _phone_nbr, busUnitId;
     rsReturn.status_nbr := -1;
     rsReturn.return_txt = 'Error: failed to update opt_in_out with intOptId= %', intOptId;
     RETURN rsReturn;
  END IF;
  ELSE
       RAISE NOTICE 'Error# -1: Invalid bus_unit_cd %', _busUnit;
     rsReturn.status_nbr := -1;
     RETURN rsReturn;
  END IF;

  
END;

$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION acc.opt_in_out_ins_updt(character varying, character varying, character varying, boolean, text, character varying)
  OWNER TO adp_dba;



