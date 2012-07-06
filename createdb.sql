--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.4
-- Dumped by pg_dump version 9.1.4
-- Started on 2012-07-07 01:02:22 CEST

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 163 (class 3079 OID 11654)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 1882 (class 0 OID 0)
-- Dependencies: 163
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 161 (class 1259 OID 16923)
-- Dependencies: 1862 1863 1864 1865 1866 1867 1868 6
-- Name: events; Type: TABLE; Schema: public; Owner: syslog; Tablespace: 
--

CREATE TABLE events (
    id integer NOT NULL,
    received_time timestamp without time zone DEFAULT now(),
    reported_time timestamp without time zone,
    host character varying(64) DEFAULT NULL::character varying,
    facility character varying(10) DEFAULT NULL::character varying,
    priority character varying(10) DEFAULT NULL::character varying,
    level character varying(10) DEFAULT NULL::character varying,
    tag character varying(10) DEFAULT NULL::character varying,
    program character varying(15) DEFAULT NULL::character varying,
    message text
);


ALTER TABLE public.events OWNER TO syslog;

--
-- TOC entry 162 (class 1259 OID 16936)
-- Dependencies: 161 6
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: syslog
--

CREATE SEQUENCE logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.logs_id_seq OWNER TO syslog;

--
-- TOC entry 1883 (class 0 OID 0)
-- Dependencies: 162
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: syslog
--

ALTER SEQUENCE logs_id_seq OWNED BY events.id;


--
-- TOC entry 1869 (class 2604 OID 16938)
-- Dependencies: 162 161
-- Name: id; Type: DEFAULT; Schema: public; Owner: syslog
--

ALTER TABLE ONLY events ALTER COLUMN id SET DEFAULT nextval('logs_id_seq'::regclass);


--
-- TOC entry 1876 (class 2606 OID 16940)
-- Dependencies: 161 161
-- Name: logs_pkey; Type: CONSTRAINT; Schema: public; Owner: syslog; Tablespace: 
--

ALTER TABLE ONLY events
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- TOC entry 1870 (class 1259 OID 16961)
-- Dependencies: 161
-- Name: events_idx_facility; Type: INDEX; Schema: public; Owner: syslog; Tablespace: 
--

CREATE INDEX events_idx_facility ON events USING btree (facility);


--
-- TOC entry 1871 (class 1259 OID 16960)
-- Dependencies: 161
-- Name: events_idx_host; Type: INDEX; Schema: public; Owner: syslog; Tablespace: 
--

CREATE INDEX events_idx_host ON events USING btree (host);


--
-- TOC entry 1872 (class 1259 OID 16962)
-- Dependencies: 161
-- Name: events_idx_priority; Type: INDEX; Schema: public; Owner: syslog; Tablespace: 
--

CREATE INDEX events_idx_priority ON events USING btree (priority);


--
-- TOC entry 1873 (class 1259 OID 16963)
-- Dependencies: 161
-- Name: events_idx_program; Type: INDEX; Schema: public; Owner: syslog; Tablespace: 
--

CREATE INDEX events_idx_program ON events USING btree (program);


--
-- TOC entry 1874 (class 1259 OID 16959)
-- Dependencies: 161
-- Name: events_idx_reported_time; Type: INDEX; Schema: public; Owner: syslog; Tablespace: 
--

CREATE INDEX events_idx_reported_time ON events USING btree (reported_time);


--
-- TOC entry 1881 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2012-07-07 01:02:22 CEST

--
-- PostgreSQL database dump complete
--

